"""Unit tests for wireguard config endpoints."""

import json

import pytest
import responses

from ponika.endpoints.wireguard.config import (
    WireguardConfigCreatePayload,
    WireguardConfigUpdatePayload,
)
from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


def _request_json_body(call_index: int) -> dict:
    body = responses.calls[call_index].request.body
    if body is None:
        return {}
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    return json.loads(body)


WIREGUARD_CONFIG_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'wg0',
            'enabled': '1',
            'private_key': 'a' * 44,
            'public_key': 'b' * 44,
            'listen_port': '51820',
            'addresses': ['10.0.0.1/24'],
            'metric': '10',
            'mtu': '1420',
            'dns': ['1.1.1.1'],
            'watchdog_interval': '5',
        }
    ],
}

WIREGUARD_CONFIG_SINGLE_RESPONSE = {
    'success': True,
    'data': WIREGUARD_CONFIG_LIST_RESPONSE['data'][0],
}

WIREGUARD_CONFIG_DELETE_RESPONSE = {
    'success': True,
    'data': {'id': 'wg0'},
}

WIREGUARD_CONFIG_BULK_DELETE_RESPONSE = {
    'success': True,
    'data': [{'id': 'wg0'}, {'id': 'wg1'}],
}


@pytest.mark.unit
@responses.activate
def test_wireguard_config_get_list(mock_client):
    mock_endpoint('get', '/wireguard/config', WIREGUARD_CONFIG_LIST_RESPONSE)

    result = mock_client.wireguard.config.get_config()

    assert len(result) == 1
    assert result[0].id == 'wg0'
    assert result[0].enabled is True


@pytest.mark.unit
@responses.activate
def test_wireguard_config_get_single(mock_client):
    mock_endpoint(
        'get',
        '/wireguard/config/wg0',
        WIREGUARD_CONFIG_SINGLE_RESPONSE,
    )

    result = mock_client.wireguard.config.get_config('wg0')

    assert result.id == 'wg0'
    assert result.listen_port == '51820'


@pytest.mark.unit
@responses.activate
def test_wireguard_config_create(mock_client):
    mock_endpoint(
        'post',
        '/wireguard/config',
        WIREGUARD_CONFIG_SINGLE_RESPONSE,
    )

    payload = WireguardConfigCreatePayload(
        id='wg0',
        enabled=True,
        private_key='a' * 44,
        listen_port='51820',
        addresses=['10.0.0.1/24'],
    )
    result = mock_client.wireguard.config.create(payload)

    assert result.id == 'wg0'

    request_body = _request_json_body(1)
    assert request_body['data']['enabled'] == '1'
    assert request_body['data']['id'] == 'wg0'


@pytest.mark.unit
@responses.activate
def test_wireguard_config_update(mock_client):
    mock_endpoint(
        'put',
        '/wireguard/config/wg0',
        WIREGUARD_CONFIG_SINGLE_RESPONSE,
    )

    payload = WireguardConfigUpdatePayload(
        id='wg0',
        enabled=False,
        private_key='a' * 44,
        metric='20',
    )
    result = mock_client.wireguard.config.update(payload)

    assert result.id == 'wg0'

    request_body = _request_json_body(1)
    assert request_body['data']['enabled'] == '0'
    assert 'id' not in request_body['data']


@pytest.mark.unit
@responses.activate
def test_wireguard_config_delete(mock_client):
    mock_endpoint(
        'delete',
        '/wireguard/config/wg0',
        WIREGUARD_CONFIG_DELETE_RESPONSE,
    )

    result = mock_client.wireguard.config.delete('wg0')

    assert result.id == 'wg0'


@pytest.mark.unit
@responses.activate
def test_wireguard_config_update_bulk(mock_client):
    bulk_response = {
        'success': True,
        'data': [
            WIREGUARD_CONFIG_LIST_RESPONSE['data'][0],
            {
                **WIREGUARD_CONFIG_LIST_RESPONSE['data'][0],
                'id': 'wg1',
                'enabled': '0',
            },
        ],
    }
    mock_endpoint('put', '/wireguard/config', bulk_response)

    payloads = [
        WireguardConfigUpdatePayload(
            id='wg0',
            enabled=True,
            private_key='a' * 44,
        ),
        WireguardConfigUpdatePayload(
            id='wg1',
            enabled=False,
            private_key='c' * 44,
        ),
    ]
    result = mock_client.wireguard.config.update_bulk(payloads)

    assert len(result) == 2
    assert result[1].id == 'wg1'

    request_body = _request_json_body(1)
    assert request_body['data'][0]['id'] == 'wg0'
    assert request_body['data'][0]['enabled'] == '1'
    assert request_body['data'][1]['enabled'] == '0'


@pytest.mark.unit
@responses.activate
def test_wireguard_config_delete_bulk(mock_client):
    mock_endpoint(
        'delete',
        '/wireguard/config',
        WIREGUARD_CONFIG_BULK_DELETE_RESPONSE,
    )

    result = mock_client.wireguard.config.delete_bulk(['wg0', 'wg1'])

    assert result[0].id == 'wg0'
    assert result[1].id == 'wg1'

    request_body = _request_json_body(1)
    assert request_body['data'] == ['wg0', 'wg1']


@pytest.mark.unit
@responses.activate
def test_wireguard_config_error_raises(mock_client):
    mock_error_response(
        'get',
        '/wireguard/config',
        error_code=122,
        error_message='Not found',
        error_source='wireguard',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.wireguard.config.get_config()
