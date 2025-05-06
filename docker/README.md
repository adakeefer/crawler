# Web Crawler Infrastructure

This directory contains the Docker Compose configuration for the web crawler's infrastructure, including external resources and crawler components.

## Services

### Redis (URL Queue)
- Port: 6379
- No authentication by default (local dev)
- Used for URL queue and worker coordination
- Health check: Redis PING every 5s

### MinIO (Content Storage)
- API: http://localhost:9000
- Console: http://localhost:9001
- Credentials: minioadmin/minioadmin
- S3-compatible storage for crawled content
- Health check: HTTP GET /minio/health/live every 5s

### MongoDB (Link Storage)
- Port: 27017
- Credentials: root/example
- Stores crawled URLs and their relationships
- Health check: MongoDB ping every 5s

### URL Frontier
- Builds from crawler/components/url_frontier
- Connects to Redis for URL queue access
- Depends on Redis service health
- Environment variables:
  - REDIS_HOST: redis
  - REDIS_PORT: 6379

### Worker
- Builds from crawler/components/worker
- Connects to Redis, MongoDB, and MinIO
- Depends on all external service health
- Environment variables:
  - REDIS_HOST: redis
  - REDIS_PORT: 6379
  - MONGODB_URI: mongodb://root:example@mongodb:27017/
  - MINIO_ENDPOINT: minio:9000
  - MINIO_ACCESS_KEY: minioadmin
  - MINIO_SECRET_KEY: minioadmin

## Usage

1. Start all services:
```bash
docker-compose up -d
```

2. Start specific services:
```bash
docker-compose up -d redis mongodb minio  # External resources only
docker-compose up -d url-frontier        # URL frontier only
docker-compose up -d worker              # Worker only
```

3. Scale workers:
```bash
docker-compose up -d --scale worker=3    # Run 3 worker instances
```

4. Check service health:
```bash
docker-compose ps
```

5. View logs:
```bash
docker-compose logs -f [service_name]
```

6. Stop services:
```bash
docker-compose down
```

## Development Notes

- Services have health checks configured
- Default credentials are for development only
- Production deployment should use proper secrets management
- Components are built from their respective directories
- Worker instances can be scaled independently 