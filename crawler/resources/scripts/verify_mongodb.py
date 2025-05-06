#!/usr/bin/env python3
import sys
from pathlib import Path
from pymongo import MongoClient
from pymongo.errors import OperationFailure

# Add parent directory to path so we can import our schemas
sys.path.append(str(Path(__file__).parent.parent))
from schemas.mongodb_schema import LinkDocument, ContentDocument

def verify_mongodb(mongo_uri: str = "mongodb://localhost:27017/"):
    """Verify MongoDB configuration matches our schema."""
    client = MongoClient(mongo_uri)
    db = client.crawler
    
    print("Verifying MongoDB configuration...")
    
    # Verify link storage
    links = db.links
    link_indexes = list(links.list_indexes())
    expected_link_indexes = LinkDocument.Config.json_schema_extra["indexes"]
    
    print("\nLink Storage:")
    print(f"Collection exists: {links.name in db.list_collection_names()}")
    print(f"Found {len(link_indexes)} indexes (expected: {len(expected_link_indexes)})")
    
    for index in expected_link_indexes:
        index_name = "_".join(f"{k}_{v}" for k, v in index["fields"])
        found = any(idx["name"] == index_name for idx in link_indexes)
        print(f"Index '{index_name}': {'✓' if found else '✗'}")
    
    # Verify content storage
    content = db.content
    content_indexes = list(content.list_indexes())
    expected_content_indexes = ContentDocument.Config.json_schema_extra["indexes"]
    
    print("\nContent Storage:")
    print(f"Collection exists: {content.name in db.list_collection_names()}")
    print(f"Found {len(content_indexes)} indexes (expected: {len(expected_content_indexes)})")
    
    for index in expected_content_indexes:
        index_name = "_".join(f"{k}_{v}" for k, v in index["fields"])
        found = any(idx["name"] == index_name for idx in content_indexes)
        print(f"Index '{index_name}': {'✓' if found else '✗'}")
    
    print("\nMongoDB verification complete!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Verify MongoDB configuration for web crawler")
    parser.add_argument("--mongo-uri", default="mongodb://localhost:27017/", help="MongoDB URI")
    args = parser.parse_args()
    
    verify_mongodb(args.mongo_uri) 