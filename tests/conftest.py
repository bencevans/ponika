"""Shared test fixtures and configuration."""

import pytest
import responses
from ponika import PonikaClient

# Base URL for mocked API
BASE_URL = 'https://test-device:443/api'

# Standard login response for mocked tests
# fmt: off
LOGIN_RESPONSE = {
    "success": True,
    "data": {
        "username": "admin",
        "token": "test-token-123",
        "expires": 3600
    }
}


@pytest.fixture
def mock_client():
    """Create a PonikaClient instance for testing with mocks.

    This client uses a fake device URL and credentials. The actual
    HTTP requests will be mocked using the @responses.activate decorator.
    """
    return PonikaClient(
        host="test-device",
        username="admin",
        password="admin",
        verify_tls=False,
    )


def mock_login():
    """Register the standard login mock response.

    Must be called within a @responses.activate context.
    """
    responses.post(
        f"{BASE_URL}/login",
        json=LOGIN_RESPONSE,
        status=200,
    )
