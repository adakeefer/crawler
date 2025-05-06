import redis
import pymongo
from minio import Minio
import time
import sys

def test_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("[OK] Redis connection successful")
        return True
    except Exception as e:
        print(f"[ERROR] Redis connection failed: {e}")
        return False

def test_mongodb():
    try:
        client = pymongo.MongoClient(
            "mongodb://root:example@localhost:27017/",
            serverSelectionTimeoutMS=2000
        )
        client.server_info()
        print("[OK] MongoDB connection successful")
        return True
    except Exception as e:
        print(f"[ERROR] MongoDB connection failed: {e}")
        return False

def test_minio():
    try:
        client = Minio(
            "localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False
        )
        client.list_buckets()
        print("[OK] MinIO connection successful")
        return True
    except Exception as e:
        print(f"[ERROR] MinIO connection failed: {e}")
        return False

def wait_for_services(max_retries=30, delay=2):
    print("Waiting for services to be ready...")
    for i in range(max_retries):
        if all([test_redis(), test_mongodb(), test_minio()]):
            print("\nAll services are ready!")
            return True
        print(f"\nRetry {i+1}/{max_retries} in {delay} seconds...")
        time.sleep(delay)
    return False

if __name__ == "__main__":
    if not wait_for_services():
        print("[ERROR] Services failed to start properly")
        sys.exit(1) 