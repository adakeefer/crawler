# External Resources

This directory contains all code related to external resources used by the web crawler.

## Schemas

The `schemas` directory contains Pydantic models defining the structure of data stored in each external resource:
- `mongodb_schema.py`: Link storage schema
- `redis_schema.py`: URL queue and worker queue schemas
- `minio_schema.py`: Content storage schema

## Initialization Scripts

The `scripts` directory contains scripts to initialize and verify each external resource:

### Redis
- `init_redis.py`: Sets up Redis queues and configuration
- `verify_redis.py`: Verifies Redis configuration and queues

### MongoDB
- `init_mongodb.py`: Creates collections and indexes
- `verify_mongodb.py`: Verifies MongoDB collections and indexes

### MinIO
- `init_minio.py`: Creates buckets and lifecycle rules
- `verify_minio.py`: Verifies MinIO buckets and configuration

## Usage

1. Initialize resources:
```bash
# Initialize all resources
python resources/scripts/init_redis.py
python resources/scripts/init_mongodb.py
python resources/scripts/init_minio.py

# Verify initialization
python resources/scripts/verify_redis.py
python resources/scripts/verify_mongodb.py
python resources/scripts/verify_minio.py
```

2. Use schemas in components:
```python
from resources.schemas.redis_schema import RedisConfig
from resources.schemas.mongodb_schema import LinkDocument
from resources.schemas.minio_schema import ContentMetadata
```

## Resource Configuration

Each resource has its own configuration in the schema files:
- Redis: Queue names, TTLs, memory settings
- MongoDB: Collection names, indexes, TTLs
- MinIO: Bucket names, lifecycle rules

See individual schema files for detailed configuration options. 