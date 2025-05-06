import os
import redis
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class URLFrontier:
    def __init__(self):
        self.redis_client = None
        
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

    def start(self):
        logger.info("Starting URL frontier process...")
        
        # Connect to Redis
        redis_connected = self.connect_to_redis()
        
        if redis_connected:
            logger.info("URL frontier successfully connected to Redis")
        else:
            logger.error("URL frontier failed to connect to Redis")
            return False
        
        return True

if __name__ == "__main__":
    frontier = URLFrontier()
    frontier.start() 