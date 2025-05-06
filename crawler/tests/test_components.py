import pytest
from unittest.mock import patch, MagicMock
from crawler.components.worker.worker import Worker
from crawler.components.url_frontier.url_frontier import URLFrontier

@pytest.fixture
def mock_redis():
    with patch('redis.Redis') as mock:
        mock_instance = MagicMock()
        mock_instance.ping.return_value = True
        mock.return_value = mock_instance
        yield mock

@pytest.fixture
def mock_mongo():
    with patch('pymongo.MongoClient') as mock:
        mock_instance = MagicMock()
        mock_instance.admin.command.return_value = True
        mock.return_value = mock_instance
        yield mock

@pytest.fixture
def mock_minio():
    with patch('crawler.components.worker.worker.Minio') as mock:
        mock_instance = MagicMock()
        mock_instance.list_buckets.return_value = []
        mock.return_value = mock_instance
        yield mock

def test_worker_connections(mock_redis, mock_mongo, mock_minio):
    worker = Worker()
    assert worker.start() is True
    
    # Verify all connections were attempted
    mock_redis.assert_called_once()
    mock_mongo.assert_called_once()
    mock_minio.assert_called_once()

def test_worker_redis_failure(mock_redis, mock_mongo, mock_minio):
    mock_redis.return_value.ping.side_effect = Exception("Connection failed")
    worker = Worker()
    assert worker.start() is False

def test_url_frontier_connections(mock_redis):
    frontier = URLFrontier()
    assert frontier.start() is True
    
    # Verify Redis connection was attempted
    mock_redis.assert_called_once()

def test_url_frontier_redis_failure(mock_redis):
    mock_redis.return_value.ping.side_effect = Exception("Connection failed")
    frontier = URLFrontier()
    assert frontier.start() is False 