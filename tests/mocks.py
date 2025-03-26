# mocks.py

import json
import pytest
from unittest.mock import AsyncMock

from conftest import (
    mock_post_response_success,
    mock_response_error_400,
    mock_response_error_403,
    mock_response_error_502,
)


async def mock_post_request_success(url, headers=None, json=None):
    """Mock a successful aiohttp POST request."""
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.__aenter__.return_value = mock_response  # mock async context manager
    mock_response.json.return_value = json.loads(mock_post_response_success)
    print("Mocked POST request success")
    return mock_response

async def mock_post_request_error_400(url, headers=None, json=None):
    # Simulate a response with an error message
    mock_response = AsyncMock()
    mock_response.status = 400
    mock_response.json = AsyncMock(return_value={"error": {"message": "Invalid transaction"}})
    return mock_response

async def mock_post_request_error_403(*args, **kwargs):
    """Mock a Forbidden access error response (403)."""
    response = AsyncMock()
    response.status = 403
    response.json = AsyncMock(return_value=json.loads(mock_response_error_403))
    return response

async def mock_post_request_error_502(*args, **kwargs):
    """Mock a Bad Gateway error response (502)."""
    response = AsyncMock()
    response.status = 502
    response.json = AsyncMock(return_value=json.loads(mock_response_error_502))
    return response
