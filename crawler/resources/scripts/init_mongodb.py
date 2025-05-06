#!/usr/bin/env python3
import sys
from pathlib import Path
from pymongo import MongoClient
from pymongo.errors import OperationFailure

# Add parent directory to path so we can import our schemas
sys.path.append(str(Path(__file__).parent.parent.parent))
from resources.schemas.mongodb_schema import LinkDocument, ContentDocument

def init_mongodb(mongo_uri: str = "mongodb://localhost:27017/"):
    """Initialize MongoDB with our schema configuration."""
    client = MongoClient(mongo_uri)
    db = client.crawler
    
    # Initialize link storage
    links = db.links
    try:
        # Drop existing indexes
        links.drop_indexes()
        
        # Create indexes from schema
        for index in LinkDocument.Config.json_schema_extra["indexes"]:
            links.create_index(
                index["fields"],
                unique=index.get("unique", False),
                expireAfterSeconds=index.get("expireAfterSeconds")
            )
    except OperationFailure as e:
        print(f"Error creating link indexes: {e}")
    
    # Initialize content storage
    content = db.content
    try:
        # Drop existing indexes
        content.drop_indexes()
        
        # Create indexes from schema
        for index in ContentDocument.Config.json_schema_extra["indexes"]:
            content.create_index(
                index["fields"],
                unique=index.get("unique", False),
                expireAfterSeconds=index.get("expireAfterSeconds")
            )
    except OperationFailure as e:
        print(f"Error creating content indexes: {e}")
    
    print("MongoDB initialized successfully!")
    print("Created collections:")
    print(f"- {links.name} with indexes: {list(links.list_indexes())}")
    print(f"- {content.name} with indexes: {list(content.list_indexes())}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Initialize MongoDB for web crawler")
    parser.add_argument("--mongo-uri", default="mongodb://localhost:27017/", help="MongoDB URI")
    args = parser.parse_args()
    
    init_mongodb(args.mongo_uri) 