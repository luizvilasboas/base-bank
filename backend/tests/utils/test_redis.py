import pytest
from unittest.mock import patch, MagicMock
from src.utils.redis import set_data, get_data, delete_data
import json


@pytest.fixture
def mock_redis_client(mocker):
    mock_redis = mocker.patch('src.utils.redis.redis_client', autospec=True)
    return mock_redis


def test_set_data(mock_redis_client):
    mock_redis_client.set.return_value = True
    key = "test_key"
    value = {"name": "test_value"}

    set_data(key, value)

    mock_redis_client.set.assert_called_once_with(
        key, json.dumps(value), ex=300)


def test_set_data_exception(mock_redis_client):
    mock_redis_client.set.side_effect = Exception("Redis error")

    key = "test_key"
    value = {"name": "test_value"}

    set_data(key, value)

    mock_redis_client.set.assert_called_once()


def test_get_data(mock_redis_client):
    key = "test_key"
    expected_value = {"name": "test_value"}
    mock_redis_client.get.return_value = json.dumps(expected_value)

    result = get_data(key)

    mock_redis_client.get.assert_called_once_with(key)

    assert result == expected_value


def test_get_data_none(mock_redis_client):
    mock_redis_client.get.return_value = None

    result = get_data("non_existent_key")

    mock_redis_client.get.assert_called_once()

    assert result is None


def test_get_data_exception(mock_redis_client):
    mock_redis_client.get.side_effect = Exception("Redis error")

    result = get_data("test_key")

    mock_redis_client.get.assert_called_once()
    assert result is None


def test_delete_data(mock_redis_client):
    key = "test_key"

    delete_data(key)

    mock_redis_client.delete.assert_called_once_with(key)


def test_delete_data_exception(mock_redis_client):
    mock_redis_client.delete.side_effect = Exception("Redis error")

    delete_data("test_key")

    mock_redis_client.delete.assert_called_once()
