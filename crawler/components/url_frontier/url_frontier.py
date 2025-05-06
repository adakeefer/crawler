import os
import redis
import logging
import sys
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class URLFrontier:
    def __init__(self):
        self.redis_client = None
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

    def health_check(self):
        """Run health check and exit with appropriate status code."""
        try:
            if not self.redis_client:
                self.connect_to_redis()
            self.redis_client.ping()
            sys.exit(0)  # Healthy
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            sys.exit(1)  # Unhealthy

    def run(self):
        """Main run loop."""
        self.running = True
        while self.running:
            # TODO: Implement URL frontier logic
            time.sleep(1)  # Prevent CPU spinning

    def start(self):
        logger.info("Starting URL frontier process...")
        
        # Connect to Redis
        redis_connected = self.connect_to_redis()
        
        if redis_connected:
            logger.info("URL frontier successfully connected to Redis")
            self.run()
        else:
            logger.error("URL frontier failed to connect to Redis")
            return False
        
        return True

if __name__ == "__main__":
    frontier = URLFrontier()
    if "--health-check" in sys.argv:
        frontier.health_check()
    else:
        frontier.start() 