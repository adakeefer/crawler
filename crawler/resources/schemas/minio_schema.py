from datetime import datetime
from pydantic import BaseModel, Field

class ContentMetadata(BaseModel):
    """Schema for storing content metadata in MinIO."""
    url: str = Field(..., description="The URL this content was downloaded from")
    content_type: str = Field(..., description="MIME type of the content")
    size_bytes: int = Field(..., description="Size of the content in bytes")
    download_time: datetime = Field(default_factory=datetime.utcnow, description="When this content was downloaded")

    class Config:
        json_schema_extra = {
            "bucket_config": {
                "name": "crawler-content",
                "versioning": True,
                "lifecycle_rules": [
                    {
                        "id": "content-ttl",
                        "status": "enabled",
                        "expiration": {
                            "days": 1  # Content will be deleted after 1 day
                        }
                    }
                ]
            }
        } 