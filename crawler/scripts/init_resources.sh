#!/bin/bash

# Exit on any error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}[+]${NC} $1"
}

# Function to print error
print_error() {
    echo -e "${RED}[-]${NC} $1"
}

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
RESOURCES_DIR="$SCRIPT_DIR/../resources/scripts"

# Initialize resources
print_status "Initializing resources..."

print_status "Initializing Redis..."
python3 "$RESOURCES_DIR/init_redis.py"

print_status "Initializing MongoDB..."
python3 "$RESOURCES_DIR/init_mongodb.py"

print_status "Initializing MinIO..."
python3 "$RESOURCES_DIR/init_minio.py"

# Verify resources
print_status "\nVerifying resources..."

print_status "Verifying Redis..."
python3 "$RESOURCES_DIR/verify_redis.py"

print_status "Verifying MongoDB..."
python3 "$RESOURCES_DIR/verify_mongodb.py"

print_status "Verifying MinIO..."
python3 "$RESOURCES_DIR/verify_minio.py"

print_status "\nAll resources initialized and verified successfully!" 