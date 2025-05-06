#!/usr/bin/env python3
import redis
import sys
from pathlib import Path

# Add parent directory to path so we can import our schemas
sys.path.append(str(Path(__file__).parent.parent))
from schemas.redis_schema import RedisConfig

def verify_redis(redis_url: str = "redis://localhost:6379"):
    """Verify Redis configuration matches our schema."""
    r = redis.from_url(redis_url)
    config = RedisConfig()
    
    # Verify Redis server settings
    maxmemory = r.config_get("maxmemory")["maxmemory"]
    maxmemory_policy = r.config_get("maxmemory-policy")["maxmemory-policy"]
    notify_keyspace_events = r.config_get("notify-keyspace-events")["notify-keyspace-events"]
    
    print("Verifying Redis configuration...")
    print(f"Max memory: {maxmemory} (expected: {config.json_schema_extra['redis_config']['maxmemory']})")
    print(f"Memory policy: {maxmemory_policy} (expected: {config.json_schema_extra['redis_config']['maxmemory_policy']})")
    print(f"Keyspace events: {notify_keyspace_events} (expected: {config.json_schema_extra['redis_config']['notify_keyspace_events']})")
    
    # Verify URL frontier queue exists
    url_queue = config.url_queue
    if not r.exists(url_queue.main_queue):
        print(f"Warning: Main URL queue '{url_queue.main_queue}' does not exist")
    
    # Verify priority queues exist
    for priority, queue_config in url_queue.priority_queues.items():
        if not r.exists(queue_config.name):
            print(f"Warning: Priority queue '{queue_config.name}' does not exist")
    
    # Verify worker queue format
    worker_config = config.worker_queues
    worker_queues = r.keys(f"{worker_config.queue_name_format.format(id='*')}")
    print(f"Found {len(worker_queues)} worker queues")
    
    # Verify domain key prefix
    domain_config = config.domain
    domain_keys = r.keys(f"{domain_config.key_prefix}*")
    print(f"Found {len(domain_keys)} domain mappings")
    
    print("\nRedis verification complete!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Verify Redis configuration for web crawler")
    parser.add_argument("--redis-url", default="redis://localhost:6379", help="Redis URL")
    args = parser.parse_args()
    
    verify_redis(args.redis_url) 