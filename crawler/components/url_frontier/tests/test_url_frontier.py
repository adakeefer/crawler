import pytest
from unittest.mock import patch, MagicMock
from crawler.components.url_frontier.url_frontier import URLFrontier

@pytest.fixture
def mock_redis():
    with patch('redis.Redis') as mock:
        mock_instance = MagicMock()
        mock_instance.ping.return_value = True
        mock.return_value = mock_instance
        yield mock

def test_url_frontier_connections(mock_redis):
    frontier = URLFrontier()
    assert frontier.start() is True
    
    # Verify Redis connection was attempted
    mock_redis.assert_called_once()

def test_url_frontier_redis_failure(mock_redis):
    mock_redis.return_value.ping.side_effect = Exception("Connection failed")
    frontier = URLFrontier()
    assert frontier.start() is False 