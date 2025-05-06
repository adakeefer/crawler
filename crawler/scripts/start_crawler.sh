#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    local name=$1
    local status=$2
    if [[ $status == *"healthy"* ]]; then
        echo -e "${GREEN}✓${NC} $name: $status"
    else
        echo -e "${RED}✗${NC} $name: $status"
    fi
}

# Function to check if all services are healthy
check_health() {
    local all_healthy=true
    local services=("redis" "mongodb" "minio" "url-frontier" "worker")
    
    for service in "${services[@]}"; do
        local status=$(docker-compose ps $service --format "{{.Status}}")
        if [[ ! $status == *"healthy"* ]]; then
            all_healthy=false
            print_status $service "$status"
        else
            print_status $service "$status"
        fi
    done
    
    return $([ "$all_healthy" = true ])
}

# Navigate to docker directory
cd "$(dirname "$0")/../../docker"

echo -e "${YELLOW}Starting crawler services...${NC}"

# Build and start services
echo -e "\n${YELLOW}Building and starting services...${NC}"
docker-compose up -d --build --scale worker=2

# Wait for services to be healthy
echo -e "\n${YELLOW}Waiting for services to be healthy...${NC}"
attempt=1
max_attempts=4  # 4 attempts * 15 seconds = 1 minute

while [ $attempt -le $max_attempts ]; do
    echo -e "\nAttempt $attempt of $max_attempts:"
    if check_health; then
        echo -e "\n${GREEN}All services are healthy!${NC}"
        exit 0
    fi
    
    if [ $attempt -lt $max_attempts ]; then
        echo -e "\n${YELLOW}Waiting 15 seconds before next attempt...${NC}"
        sleep 15
    fi
    
    attempt=$((attempt + 1))
done

echo -e "\n${RED}Failed to get all services healthy within 1 minute${NC}"
exit 1 