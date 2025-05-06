from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class LinkDocument(BaseModel):
    """Schema for storing links in MongoDB."""
    url: str = Field(..., description="The URL that was crawled")
    parent_url: Optional[str] = Field(None, description="The URL that led to this URL")

    class Config:
        json_schema_extra = {
            "indexes": [
                {"fields": ["url"], "unique": True},
                {"fields": ["_id"], "expireAfterSeconds": 3600}  # 1 hour TTL on _id
            ]
        }

class ContentDocument(BaseModel):
    """Schema for storing content metadata and fingerprints in MongoDB."""
    url: str = Field(..., description="The URL this content was downloaded from")
    minio_path: str = Field(..., description="Path to content in MinIO")
    content_type: str = Field(..., description="MIME type of the content")
    size_bytes: int = Field(..., description="Size of the content in bytes")
    download_time: datetime = Field(default_factory=datetime.utcnow, description="When this content was downloaded")
    content_hash: str = Field(..., description="SHA-256 hash of content for exact matching")
    simhash: int = Field(..., description="64-bit SimHash of content for similarity detection")
    
    class Config:
        json_schema_extra = {
            "indexes": [
                {"fields": ["url"], "unique": True},
                {"fields": ["content_hash"], "unique": True},  # For exact matches
                {"fields": ["simhash"]},  # For similarity lookup
                {"fields": ["_id"], "expireAfterSeconds": 3600}  # 1 hour TTL
            ]
        } 