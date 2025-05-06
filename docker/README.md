# Web Crawler Infrastructure

This directory contains the Docker Compose configuration for the web crawler's external resources.

## Services

### Redis (URL Queue)
- Port: 6379
- No authentication by default (local dev)
- Persistence enabled with AOF
- Used for URL queue and worker coordination

### MinIO (Content Storage)
- API: http://localhost:9000
- Console: http://localhost:9001
- Credentials: minioadmin/minioadmin
- S3-compatible storage for crawled content

### MongoDB (Link Storage)
- Port: 27017
- Credentials: root/example
- Stores crawled URLs and their relationships

## Usage

1. Start services:
```bash
docker-compose up -d
```

2. Check service health:
```bash
docker-compose ps
```

3. View logs:
```bash
docker-compose logs -f [service_name]
```

4. Stop services:
```bash
docker-compose down
```

## Development Notes

- All data is persisted in Docker volumes
- Services have health checks configured
- Default credentials are for development only
- Production deployment should use proper secrets management 