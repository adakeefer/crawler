import os
import redis
import pymongo
from minio import Minio
import logging
import sys
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Worker:
    def __init__(self):
        self.redis_client = None
        self.mongo_client = None
        self.minio_client = None
        self.running = False
        
    def connect_to_redis(self):
        try:
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                decode_responses=True
            )
            self.redis_client.ping()
            logger.info("Successfully connected to Redis")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return False

    def connect_to_mongodb(self):
        try:
            self.mongo_client = pymongo.MongoClient(
                os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
            )
            self.mongo_client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False

    def connect_to_minio(self):
        try:
            self.minio_client = Minio(
                endpoint=os.getenv('MINIO_ENDPOINT', 'localhost:9000'),
                access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
                secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin'),
                secure=False
            )
            self.minio_client.list_buckets()
            logger.info("Successfully connected to MinIO")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MinIO: {e}")
            return False

    def health_check(self):
        """Run health check and exit with appropriate status code."""
        try:
            if not self.redis_client:
                self.connect_to_redis()
            if not self.mongo_client:
                self.connect_to_mongodb()
            if not self.minio_client:
                self.connect_to_minio()
                
            # Check all connections
            self.redis_client.ping()
            self.mongo_client.admin.command('ping')
            self.minio_client.list_buckets()
            
            sys.exit(0)  # Healthy
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            sys.exit(1)  # Unhealthy

    def run(self):
        """Main run loop."""
        self.running = True
        while self.running:
            # TODO: Implement worker logic
            time.sleep(1)  # Prevent CPU spinning

    def start(self):
        logger.info("Starting worker process...")
        
        # Connect to all services
        redis_connected = self.connect_to_redis()
        mongo_connected = self.connect_to_mongodb()
        minio_connected = self.connect_to_minio()
        
        if all([redis_connected, mongo_connected, minio_connected]):
            logger.info("Worker successfully connected to all services")
            self.run()
        else:
            logger.error("Worker failed to connect to one or more services")
            return False
        
        return True

if __name__ == "__main__":
    worker = Worker()
    if "--health-check" in sys.argv:
        worker.health_check()
    else:
        worker.start() 