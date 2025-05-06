# URL Frontier Component

The URL Frontier is responsible for managing and distributing URLs to worker instances. It reads from the Distributed URL queue, prioritizes URLs, and distributes them to worker queues based on domain and load.

## Dependencies
- Redis: For URL queue and worker coordination

## Environment Variables
- `REDIS_HOST`: Redis server hostname (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)

## Running with Docker
```bash
# Build and run with docker-compose
docker-compose up url-frontier

# Or run standalone
docker build -t url-frontier .
docker run -e REDIS_HOST=redis -e REDIS_PORT=6379 url-frontier
```

## Component Behavior
1. Connects to Redis for URL queue access
2. Continuously pulls URLs from the Distributed URL queue
3. Prioritizes URLs based on configured criteria
4. Distributes URLs to worker queues based on domain and load
5. Handles backpressure from worker queues

## Health Checks
- Monitors Redis connection status
- Logs connection and operational status 