import redis
import pymongo
from minio import Minio
import time
import sys

def test_redis():
    r = redis.Redis(host='localhost', port=6379, db=0)
    assert r.ping(), "Redis connection failed"
    print("[OK] Redis connection successful")

def test_mongodb():
    client = pymongo.MongoClient(
        "mongodb://root:example@localhost:27017/",
        serverSelectionTimeoutMS=2000
    )
    assert client.server_info(), "MongoDB connection failed"
    print("[OK] MongoDB connection successful")

def test_minio():
    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    # Just check if we can connect, don't assert on empty bucket list
    client.list_buckets()
    print("[OK] MinIO connection successful")

def wait_for_services(max_retries=30, delay=2):
    print("Waiting for services to be ready...")
    for i in range(max_retries):
        try:
            test_redis()
            test_mongodb()
            test_minio()
            print("\nAll services are ready!")
            return True
        except Exception as e:
            print(f"\nRetry {i+1}/{max_retries} in {delay} seconds...")
            time.sleep(delay)
    return False

if __name__ == "__main__":
    if not wait_for_services():
        print("[ERROR] Services failed to start properly")
        sys.exit(1) 