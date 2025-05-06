from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class PriorityQueueConfig(BaseModel):
    """Configuration for a single priority queue."""
    name: str = Field(..., description="Name of the priority queue")
    weight: float = Field(..., description="Weight for random selection (higher = more likely to be chosen)")

class URLQueueConfig(BaseModel):
    """Schema for Redis URL queue configuration."""
    main_queue: str = Field("url_frontier", description="Name of the main URL queue")
    max_size: int = Field(10000, description="Maximum number of URLs in the queue")
    priority_queues: Dict[int, PriorityQueueConfig] = Field(
        default={
            0: PriorityQueueConfig(name="high_priority", weight=0.6),
            1: PriorityQueueConfig(name="medium_priority", weight=0.3),
            2: PriorityQueueConfig(name="low_priority", weight=0.1)
        },
        description="Mapping of priority level to queue config"
    )

class WorkerQueueConfig(BaseModel):
    """Schema for Redis worker queue configuration."""
    queue_name_format: str = Field("worker_{id}", description="Format string for worker queue names")
    default_max_size: int = Field(10000, description="Default maximum URLs per worker queue")
    worker_max_sizes: Dict[int, int] = Field(
        default_factory=dict,
        description="Optional per-worker queue size limits"
    )
    
    def get_queue_name(self, worker_id: int) -> str:
        """Get the Redis queue name for a worker."""
        return self.queue_name_format.format(id=worker_id)
    
    def get_max_size(self, worker_id: int) -> int:
        """Get the maximum queue size for a worker."""
        return self.worker_max_sizes.get(worker_id, self.default_max_size)

class DomainConfig(BaseModel):
    """Schema for domain-specific configuration."""
    key_prefix: str = Field("domain:", description="Prefix for domain keys in Redis")
    default_ttl: int = Field(300, description="Default TTL for domain assignments in seconds (5 minutes)")
    min_ttl: int = Field(60, description="Minimum TTL for any domain in seconds")
    max_ttl: int = Field(3600, description="Maximum TTL for any domain in seconds")
    
    def get_domain_key(self, domain: str) -> str:
        """Get the Redis key for a domain."""
        return f"{self.key_prefix}{domain}"
    
    def get_worker_id(self, domain: str, redis_client) -> Optional[int]:
        """Get the worker ID assigned to a domain."""
        key = self.get_domain_key(domain)
        worker_id = redis_client.get(key)
        return int(worker_id) if worker_id else None
    
    def assign_worker(self, domain: str, worker_id: int, ttl: Optional[int] = None, redis_client=None) -> None:
        """Assign a domain to a worker with optional TTL."""
        if redis_client is None:
            raise ValueError("Redis client required for assignment")
            
        key = self.get_domain_key(domain)
        ttl = min(max(ttl or self.default_ttl, self.min_ttl), self.max_ttl)
        redis_client.set(key, worker_id, ex=ttl)

class RedisConfig(BaseModel):
    """Schema for Redis configuration."""
    url_queue: URLQueueConfig = Field(default_factory=URLQueueConfig)
    worker_queues: WorkerQueueConfig = Field(default_factory=WorkerQueueConfig)
    domain: DomainConfig = Field(default_factory=DomainConfig)

    class Config:
        json_schema_extra = {
            "redis_config": {
                "maxmemory": "1gb",
                "maxmemory_policy": "allkeys-lru",
                "notify_keyspace_events": "Ex"  # Enable key expiration events
            }
        } 