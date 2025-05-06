#!/usr/bin/env python3
import redis
import sys
from pathlib import Path

# Add parent directory to path so we can import our schemas
sys.path.append(str(Path(__file__).parent.parent))
from schemas.redis_schema import RedisConfig

def init_redis(redis_url: str = "redis://localhost:6379"):
    """Initialize Redis with our schema configuration."""
    r = redis.from_url(redis_url)
    config = RedisConfig()
    
    # Configure Redis server settings
    r.config_set("maxmemory", config.json_schema_extra["redis_config"]["maxmemory"])
    r.config_set("maxmemory-policy", config.json_schema_extra["redis_config"]["maxmemory_policy"])
    r.config_set("notify-keyspace-events", config.json_schema_extra["redis_config"]["notify_keyspace_events"])
    
    # Initialize URL frontier queue
    url_queue = config.url_queue
    r.delete(url_queue.main_queue)  # Clear existing queue
    for priority, queue_config in url_queue.priority_queues.items():
        r.delete(queue_config.name)  # Clear existing priority queues
    
    # Initialize worker queues
    worker_config = config.worker_queues
    # Get all existing worker queues and clear them
    existing_queues = r.keys(f"{worker_config.queue_name_format.format(id='*')}")
    for queue in existing_queues:
        r.delete(queue)
    
    # Clear domain mappings
    domain_config = config.domain
    existing_domains = r.keys(f"{domain_config.key_prefix}*")
    for domain in existing_domains:
        r.delete(domain)
    
    print("Redis initialized successfully!")
    print(f"Main URL queue: {url_queue.main_queue}")
    print(f"Priority queues: {[q.name for q in url_queue.priority_queues.values()]}")
    print(f"Worker queue format: {worker_config.queue_name_format}")
    print(f"Domain key prefix: {domain_config.key_prefix}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Initialize Redis for web crawler")
    parser.add_argument("--redis-url", default="redis://localhost:6379", help="Redis URL")
    args = parser.parse_args()
    
    init_redis(args.redis_url) 