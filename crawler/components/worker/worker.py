import os
import redis
import pymongo
from minio import Minio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Worker:
    def __init__(self):
        self.redis_client = None
        self.mongo_client = None
        self.minio_client = None
        
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

    def start(self):
        logger.info("Starting worker process...")
        
        # Connect to all services
        redis_connected = self.connect_to_redis()
        mongo_connected = self.connect_to_mongodb()
        minio_connected = self.connect_to_minio()
        
        if all([redis_connected, mongo_connected, minio_connected]):
            logger.info("Worker successfully connected to all services")
        else:
            logger.error("Worker failed to connect to one or more services")
            return False
        
        return True

if __name__ == "__main__":
    worker = Worker()
    worker.start() 