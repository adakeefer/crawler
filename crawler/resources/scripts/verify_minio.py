#!/usr/bin/env python3
import sys
from pathlib import Path
from minio import Minio
from minio.error import S3Error
from minio.lifecycleconfig import Rule, Expiration, Filter

# Add parent directory to path so we can import our schemas
sys.path.append(str(Path(__file__).parent.parent))
from schemas.minio_schema import ContentMetadata

def verify_minio(
    endpoint: str = "localhost:9000",
    access_key: str = "minioadmin",
    secret_key: str = "minioadmin",
    secure: bool = False
):
    """Verify MinIO configuration matches our schema."""
    client = Minio(endpoint, access_key, secret_key, secure=secure)
    
    # Get bucket config from schema
    bucket_config = ContentMetadata.Config.json_schema_extra["bucket_config"]
    bucket_name = bucket_config["name"]
    
    print("Verifying MinIO configuration...")
    
    try:
        # Verify bucket exists
        exists = client.bucket_exists(bucket_name)
        print(f"\nBucket '{bucket_name}': {'✓' if exists else '✗'}")
        
        if exists:
            # Verify versioning
            versioning = client.get_bucket_versioning(bucket_name)
            expected_versioning = "Enabled" if bucket_config["versioning"] else "Disabled"
            print(f"Versioning: {versioning} (expected: {expected_versioning})")
            
            # Verify lifecycle rules
            lifecycle = client.get_bucket_lifecycle(bucket_name)
            expected_rules = bucket_config["lifecycle_rules"]
            
            print("\nLifecycle Rules:")
            print(f"Found {len(lifecycle.rules)} rules (expected: {len(expected_rules)})")
            
            for rule in expected_rules:
                found = any(
                    r.rule_id == rule["id"] and
                    r.status == rule["status"] and
                    r.expiration.days == rule["expiration"]["days"]
                    for r in lifecycle.rules
                )
                print(f"Rule '{rule['id']}': {'✓' if found else '✗'}")
        
        print("\nMinIO verification complete!")
        
    except S3Error as e:
        print(f"Error verifying MinIO: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Verify MinIO configuration for web crawler")
    parser.add_argument("--endpoint", default="localhost:9000", help="MinIO endpoint")
    parser.add_argument("--access-key", default="minioadmin", help="MinIO access key")
    parser.add_argument("--secret-key", default="minioadmin", help="MinIO secret key")
    parser.add_argument("--secure", action="store_true", help="Use HTTPS")
    args = parser.parse_args()
    
    verify_minio(
        endpoint=args.endpoint,
        access_key=args.access_key,
        secret_key=args.secret_key,
        secure=args.secure
    ) 