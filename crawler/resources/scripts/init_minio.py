#!/usr/bin/env python3
import sys
from pathlib import Path
from minio import Minio
from minio.error import S3Error
from minio.versioningconfig import VersioningConfig, ENABLED
from minio.lifecycleconfig import LifecycleConfig, Rule, Expiration, Filter

# Add parent directory to path so we can import our schemas
sys.path.append(str(Path(__file__).parent.parent.parent))
from resources.schemas.minio_schema import ContentMetadata

def init_minio(
    endpoint: str = "localhost:9000",
    access_key: str = "minioadmin",
    secret_key: str = "minioadmin",
    secure: bool = False
):
    """Initialize MinIO with our schema configuration."""
    client = Minio(endpoint, access_key, secret_key, secure=secure)
    
    # Get bucket config from schema
    bucket_config = ContentMetadata.Config.json_schema_extra["bucket_config"]
    bucket_name = bucket_config["name"]
    
    try:
        # Create bucket if it doesn't exist
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Created bucket: {bucket_name}")
        
        # Configure versioning
        if bucket_config["versioning"]:
            versioning = VersioningConfig(ENABLED)
            client.set_bucket_versioning(bucket_name, versioning)
            print(f"Enabled versioning for bucket: {bucket_name}")
        
        # Configure lifecycle rules
        rules = []
        for rule_config in bucket_config["lifecycle_rules"]:
            rules.append(
                Rule(
                    rule_filter=Filter(prefix=rule_config["id"]),
                    rule_id=rule_config["id"],
                    status=rule_config["status"],
                    expiration=Expiration(days=rule_config["expiration"]["days"])
                )
            )
        lifecycle = LifecycleConfig(rules)
        client.set_bucket_lifecycle(bucket_name, lifecycle)
        print(f"Set lifecycle rules for bucket: {bucket_name}")
        
        print("MinIO initialized successfully!")
        print(f"Bucket: {bucket_name}")
        print("Configuration:")
        print(f"- Versioning: {bucket_config['versioning']}")
        print(f"- Lifecycle rules: {bucket_config['lifecycle_rules']}")
        
    except S3Error as e:
        print(f"Error initializing MinIO: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Initialize MinIO for web crawler")
    parser.add_argument("--endpoint", default="localhost:9000", help="MinIO endpoint")
    parser.add_argument("--access-key", default="minioadmin", help="MinIO access key")
    parser.add_argument("--secret-key", default="minioadmin", help="MinIO secret key")
    parser.add_argument("--secure", action="store_true", help="Use HTTPS")
    args = parser.parse_args()
    
    init_minio(
        endpoint=args.endpoint,
        access_key=args.access_key,
        secret_key=args.secret_key,
        secure=args.secure
    ) 