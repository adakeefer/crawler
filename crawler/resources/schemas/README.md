# Resource Schemas

This directory contains the schema definitions for all external resources used by the web crawler.

## MongoDB Schema (`mongodb_schema.py`)

Defines the schema for link storage in MongoDB:
- `LinkDocument`: Stores information about crawled URLs
- Includes indexes for efficient querying and a 1-hour TTL
- Fields track URL metadata, visit status, and priority

## MinIO Schema (`minio_schema.py`)

Defines the schema for content storage in MinIO:
- `ContentMetadata`: Stores metadata about downloaded content
- Configures bucket with versioning and lifecycle rules
- Includes content deduplication via hashing
- Content is automatically deleted after 1 day

## Redis Schema (`redis_schema.py`)

Defines the schema for Redis queues and data structures:
- `URLQueueConfig`: Configuration for the main URL frontier queue
- `WorkerQueueConfig`: Configuration for worker-specific queues
- `RedisConfig`: Global Redis configuration including key patterns
- Includes memory management and key expiration settings

## Usage

These schemas are used by the crawler components to:
1. Validate data before storage
2. Configure external resources
3. Ensure consistent data structure across components
4. Manage resource lifecycle and cleanup

## Dependencies

- pydantic: For schema validation and configuration
- datetime: For TTL and timestamp management 