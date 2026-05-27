"""Unit tests demonstrating login parameter validation."""

import pytest
import responses
from ponika import PonikaClient

from ponika.exceptions import TeltonikaLoginException
from tests.mocks import (
    mock_endpoint,
    mock_login_with_validation,
)

# Tailscale mock responses
TAILSCALE_CONFIG_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'tailscale0',
            'enabled': '1',
            'auth_key': '',
            'advert_routes': [],
            'accept_routes': '0',
            'exit_node': '0',
            'auth_type': 'url',
            'default_route': '0',
            'exit_node_ip': '',
            'login_server': '',
        }
    ],
}


@pytest.mark.unit
@responses.activate
def test_login_with_correct_credentials():
    """Test login with correct credentials (admin/admin)."""
    # Mock login with validation enabled
    mock_login_with_validation()

    # Create client with correct credentials
    client = PonikaClient(
        host='test-device',
        username='admin',
        password='admin',
        verify_tls=False,
    )

    # Try to login (happens automatically on first request)
    responses.get(
        'https://test-device:443/api/test',
        json={'success': True, 'data': {}},
    )

    result = client._get('/test')

    # Should succeed because credentials are correct
    assert result['success'] is True


@pytest.mark.unit
@responses.activate
def test_login_with_incorrect_credentials():
    """Test login with incorrect credentials."""
    # Mock login with validation enabled
    mock_login_with_validation()

    with pytest.raises(TeltonikaLoginException):
        # Create client with incorrect credentials
        client = PonikaClient(
            host='test-device',
            username='admin',
            password='wrong',
            verify_tls=False,
        )

        # Try to get auth token
        token = client._get_auth_token()

        # Should fail because credentials are wrong
        assert token is None
        assert client.auth is None


@pytest.mark.unit
@responses.activate
def test_endpoint_with_login_validation():
    """Test that endpoint calls fail when login credentials are wrong."""
    # Use mock_endpoint with validate_login=True
    mock_endpoint(
        'get',
        '/tailscale/config',
        TAILSCALE_CONFIG_RESPONSE,
        validate_login=True,
    )

    # Create client with wrong credentials
    client = PonikaClient(
        host='test-device',
        username='admin',
        password='wrong',
        verify_tls=False,
    )

    # Try to make a request - should fail at login
    try:
        token = client._get_auth_token()
        assert token is None
    except:
        pass

    with pytest.raises(TeltonikaLoginException):
        client.tailscale.get_config()


@pytest.mark.unit
@responses.activate
def test_endpoint_with_correct_credentials_and_validation():
    """Test that endpoint calls succeed with correct credentials."""
    # Use mock_endpoint with validate_login=True
    mock_endpoint(
        'get',
        '/tailscale/config',
        TAILSCALE_CONFIG_RESPONSE,
        validate_login=True,
    )

    # Create client with correct credentials
    client = PonikaClient(
        host='test-device',
        username='admin',
        password='admin',
        verify_tls=False,
    )

    # Make request - should succeed
    result = client.tailscale.get_config()

    assert result[0].id == 'tailscale0'


@pytest.mark.unit
@responses.activate
def test_custom_parameter_validation():
    """Test custom parameter validation using callbacks."""
    import json
    from tests.mocks import mock_endpoint_with_callback

    # Define a callback that validates custom parameters
    def validate_config_update(request):
        body = json.loads(request.body)

        # Check if required 'data' parameter exists and has valid format
        if 'data' not in body:
            error = {
                'success': False,
                'errors': [
                    {
                        'code': 400,
                        'error': "Missing 'data' parameter",
                        'source': 'validation',
                        'section': None,
                    }
                ],
            }
            return (200, {}, json.dumps(error))

        data = body['data']

        # Validate that 'enabled' field is present
        if 'enabled' not in data:
            error = {
                'success': False,
                'errors': [
                    {
                        'code': 400,
                        'error': "Missing 'enabled' field",
                        'source': 'validation',
                        'section': None,
                    }
                ],
            }
            return (200, {}, json.dumps(error))

        # Valid request
        # fmt: off
        success = {
            "success": True,
            "data": {"message": "Configuration updated"}
        }
        return (200, {}, json.dumps(success))

    # Mock the endpoint with callback
    mock_endpoint_with_callback(
        'put',
        '/tailscale/config',
        callback=validate_config_update,
        validate_login=False,
    )

    # Create client
    client = PonikaClient(
        host='test-device',
        username='admin',
        password='admin',
        verify_tls=False,
    )

    # Test with valid data
    result = client._put_data(
        '/tailscale/config',
        dict,  # Simple type for response
        params={'enabled': '1'},
    )

    assert result.success

    # Test with invalid data (missing 'enabled')
    result_invalid = client._put_data(
        '/tailscale/config', dict, params={'other_field': 'value'}
    )

    assert not result_invalid.success
    assert result_invalid.errors[0].code == 400
    assert 'enabled' in result_invalid.errors[0].error
