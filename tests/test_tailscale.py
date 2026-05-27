"""Unit tests for Tailscale endpoint using mocked responses."""

import json

import pytest
import responses

from ponika.endpoints.tailscale import (
    TailscaleConfigUpdatePayload,
)
from ponika.exceptions import TeltonikaApiException
from tests.mocks import (
    mock_endpoint,
    mock_error_response,
)


def _request_json_body(call_index: int) -> dict:
    body = responses.calls[call_index].request.body
    if body is None:
        return {}
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    return json.loads(body)


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

TAILSCALE_STATUS_RESPONSE = {
    'success': True,
    'data': [
        {
            'status': 'running',
            'url': 'https://login.tailscale.com/...',
            'ip': ['100.64.0.1'],
            'message': [],
        }
    ],
}

TAILSCALE_SINGLE_CONFIG_RESPONSE = {
    'success': True,
    'data': {
        'id': 'tailscale0',
        'enabled': '1',
        'auth_key': '',
        'advert_routes': ['10.10.0.0/24'],
        'accept_routes': '1',
        'exit_node': '0',
        'auth_type': 'url',
        'default_route': '0',
        'exit_node_ip': '',
        'login_server': '',
    },
}


@pytest.mark.unit
@responses.activate
def test_tailscale_get_config_success(mock_client):
    """Test successful retrieval of Tailscale configuration."""
    mock_endpoint('get', '/tailscale/config', TAILSCALE_CONFIG_RESPONSE)

    result = mock_client.tailscale.get_config()

    assert len(result) == 1
    assert result[0].id == 'tailscale0'
    assert result[0].enabled == '1'
    assert result[0].auth_type == 'url'

    # Verify the correct endpoints were called
    assert len(responses.calls) == 2  # login + get_config
    assert (
        responses.calls[0].request.url == 'https://test-device:443/api/login'
    )
    assert (
        responses.calls[1].request.url
        == 'https://test-device:443/api/tailscale/config'
    )
    assert (
        responses.calls[1].request.headers['Authorization']
        == 'Bearer test-token-123'
    )


@pytest.mark.unit
@responses.activate
def test_tailscale_get_config_not_supported(mock_client):
    """Test Tailscale config when device doesn't support the feature."""
    mock_error_response(
        'get',
        '/tailscale/config',
        error_code=122,
        error_message='Not found',
        error_source='tailscale',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.tailscale.get_config()


@pytest.mark.unit
@responses.activate
def test_tailscale_get_status_success(mock_client):
    """Test successful retrieval of Tailscale status."""
    mock_endpoint('get', '/tailscale/status', TAILSCALE_STATUS_RESPONSE)

    result = mock_client.tailscale.get_status()

    assert len(result) == 1
    assert result[0].status == 'running'
    assert result[0].ip == ['100.64.0.1']
    assert result[0].url == 'https://login.tailscale.com/...'


@pytest.mark.unit
@responses.activate
def test_tailscale_get_status_disconnected(mock_client):
    """Test Tailscale status when disconnected."""
    disconnected_response = {
        'success': True,
        'data': [
            {
                'status': 'disconnected',
                'url': '',
                'ip': [],
                'message': ['Not authenticated'],
            }
        ],
    }

    mock_endpoint('get', '/tailscale/status', disconnected_response)

    result = mock_client.tailscale.get_status()

    assert result[0].status == 'disconnected'
    assert result[0].ip == []
    assert len(result[0].message) == 1


@pytest.mark.unit
@responses.activate
def test_tailscale_get_config_single_success(mock_client):
    """Test successful retrieval of a single Tailscale configuration by id."""
    mock_endpoint(
        'get',
        '/tailscale/config/tailscale0',
        TAILSCALE_SINGLE_CONFIG_RESPONSE,
    )

    result = mock_client.tailscale.get_config('tailscale0')

    assert result.id == 'tailscale0'
    assert result.auth_type == 'url'
    assert result.advert_routes == ['10.10.0.0/24']


@pytest.mark.unit
@responses.activate
def test_tailscale_update_config_success(mock_client):
    """Test successful update of all Tailscale configurations."""
    update_payload = [
        TailscaleConfigUpdatePayload.model_validate(
            {
                'enabled': '1',
                'auth_type': 'url',
                'advert_routes': ['10.0.0.0/24'],
                'accept_routes': '1',
                'exit_node': '0',
                'default_route': '0',
                'exit_node_ip': '',
                'login_server': '',
            }
        )
    ]

    mock_endpoint('put', '/tailscale/config', TAILSCALE_CONFIG_RESPONSE)

    result = mock_client.tailscale.update_bulk(update_payload)

    assert result[0].id == 'tailscale0'

    request_body = _request_json_body(1)
    assert 'data' in request_body
    assert isinstance(request_body['data'], list)
    assert request_body['data'][0]['auth_type'] == 'url'
    assert request_body['data'][0]['enabled'] == '1'


@pytest.mark.unit
@responses.activate
def test_tailscale_update_config_by_id_success(mock_client):
    """Test successful update of a single Tailscale configuration by id."""
    update_payload = TailscaleConfigUpdatePayload.model_validate(
        {
            'enabled': '1',
            'auth_type': 'key',
            'auth_key': 'tskey-12345678901234567890',
            'advert_routes': [],
            'accept_routes': '0',
            'exit_node': '0',
            'default_route': '0',
            'exit_node_ip': '',
            'login_server': '',
        }
    )

    mock_endpoint(
        'put',
        '/tailscale/config/tailscale0',
        TAILSCALE_SINGLE_CONFIG_RESPONSE,
    )

    result = mock_client.tailscale.update_by_id(
        item_id='tailscale0',
        payload=update_payload,
    )

    assert result.id == 'tailscale0'

    request_body = _request_json_body(1)
    assert 'data' in request_body
    assert isinstance(request_body['data'], dict)
    assert request_body['data']['auth_type'] == 'key'
    assert request_body['data']['auth_key'] == 'tskey-12345678901234567890'


@pytest.mark.unit
@responses.activate
def test_tailscale_multiple_configs(mock_client):
    """Test Tailscale with multiple configuration entries."""
    multi_config_response = {
        'success': True,
        'data': [
            {
                'id': 'tailscale0',
                'enabled': '1',
                'auth_key': '',
                'advert_routes': ['10.0.0.0/24'],
                'accept_routes': '1',
                'exit_node': '0',
                'auth_type': 'url',
                'default_route': '0',
                'exit_node_ip': '',
                'login_server': '',
            },
            {
                'id': 'tailscale1',
                'enabled': '0',
                'auth_key': 'tskey-...',
                'advert_routes': [],
                'accept_routes': '0',
                'exit_node': '0',
                'auth_type': 'key',
                'default_route': '0',
                'exit_node_ip': '',
                'login_server': 'https://custom.tailscale.com',
            },
        ],
    }

    mock_endpoint('get', '/tailscale/config', multi_config_response)

    result = mock_client.tailscale.get_config()

    assert len(result) == 2
    assert result[0].id == 'tailscale0'
    assert result[0].advert_routes == ['10.0.0.0/24']
    assert result[1].id == 'tailscale1'
    assert result[1].auth_type == 'key'
