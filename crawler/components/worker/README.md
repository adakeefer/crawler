# Worker Component

The Worker is responsible for downloading web pages, parsing content, and extracting new URLs. It processes URLs from its dedicated worker queue and publishes new URLs to the Distributed URL queue.

## Dependencies
- Redis: For worker queue access
- MongoDB: For link storage
- MinIO: For content storage

## Environment Variables
- `REDIS_HOST`: Redis server hostname (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `MONGODB_URI`: MongoDB connection string (default: mongodb://localhost:27017/)
- `MINIO_ENDPOINT`: MinIO server endpoint (default: localhost:9000)
- `MINIO_ACCESS_KEY`: MinIO access key (default: minioadmin)
- `MINIO_SECRET_KEY`: MinIO secret key (default: minioadmin)

## Running with Docker
```bash
# Build and run with docker-compose
docker-compose up worker

# Or run standalone
docker build -t worker .
docker run \
  -e REDIS_HOST=redis \
  -e REDIS_PORT=6379 \
  -e MONGODB_URI=mongodb://root:example@mongodb:27017/ \
  -e MINIO_ENDPOINT=minio:9000 \
  -e MINIO_ACCESS_KEY=minioadmin \
  -e MINIO_SECRET_KEY=minioadmin \
  worker
```

## Component Behavior
1. Connects to Redis, MongoDB, and MinIO
2. Pulls URLs from its dedicated worker queue
3. Downloads and validates web pages
4. Performs content deduplication:
   ```
   For each downloaded page:
   1. Generate SHA-256 hash of content
   2. Check MongoDB for exact match using content_hash
   3. If no exact match:
      - Generate 64-bit SimHash
      - Find similar documents in MongoDB (Hamming distance < 3)
      - If similar found, consider it a duplicate and discard
      - If no similar found, store in MinIO and MongoDB
   ```
5. Extracts and validates new URLs
6. Publishes new URLs to the Distributed URL queue

## Health Checks
- Monitors connections to Redis, MongoDB, and MinIO
- Logs connection and operational status 