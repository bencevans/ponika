"""Unit tests for wireguard peers endpoints."""

import json

import pytest
import responses

from ponika.endpoints.wireguard.peers import (
    WireguardPeerCreateItemPayload,
    WireguardPeerUpdateItemPayload,
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


WIREGUARD_PEERS_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'peer1',
            'public_key': 'p' * 44,
            'allowed_ips': ['10.10.0.2/32'],
            'route_allowed_ips': '1',
            'endpoint_host': 'example.org',
            'endpoint_port': '51820',
        }
    ],
}

WIREGUARD_PEER_SINGLE_RESPONSE = {
    'success': True,
    'data': WIREGUARD_PEERS_LIST_RESPONSE['data'][0],
}

WIREGUARD_PEER_DELETE_RESPONSE = {
    'success': True,
    'data': {'id': 'peer1'},
}

WIREGUARD_PEER_BULK_DELETE_RESPONSE = {
    'success': True,
    'data': [{'id': 'peer1'}, {'id': 'peer2'}],
}


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_config_api_crud(mock_client):
    mock_endpoint(
        'get',
        '/wireguard/wg0/peers/config',
        WIREGUARD_PEERS_LIST_RESPONSE,
    )
    mock_endpoint(
        'get',
        '/wireguard/wg0/peers/config/peer1',
        WIREGUARD_PEER_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/wireguard/wg0/peers/config',
        WIREGUARD_PEER_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/wireguard/wg0/peers/config/peer1',
        WIREGUARD_PEER_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/wireguard/wg0/peers/config/peer1',
        WIREGUARD_PEER_DELETE_RESPONSE,
        include_login=False,
    )

    endpoint = mock_client.wireguard.peers.config('wg0')

    list_result = endpoint.get_config()
    single_result = endpoint.get_config('peer1')

    create_payload = WireguardPeerCreateItemPayload(id='peer1')
    create_payload.public_key = 'p' * 44
    create_payload.allowed_ips = ['10.10.0.2/32']
    create_payload.route_allowed_ips = True
    create_result = endpoint.create(create_payload)

    update_payload = WireguardPeerUpdateItemPayload(id='peer1')
    update_payload.public_key = 'p' * 44
    update_payload.allowed_ips = ['10.10.0.3/32']
    update_payload.route_allowed_ips = False
    update_result = endpoint.update(update_payload)

    delete_result = endpoint.delete('peer1')

    assert len(list_result) == 1
    assert list_result[0].route_allowed_ips is True
    assert single_result.id == 'peer1'
    assert create_result.id == 'peer1'
    assert update_result.id == 'peer1'
    assert delete_result.id == 'peer1'

    create_body = _request_json_body(3)
    assert create_body['data']['id'] == 'peer1'
    assert create_body['data']['route_allowed_ips'] == '1'

    update_body = _request_json_body(4)
    assert 'id' not in update_body['data']
    assert update_body['data']['route_allowed_ips'] == '0'


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_config_api_bulk(mock_client):
    bulk_response = {
        'success': True,
        'data': [
            WIREGUARD_PEERS_LIST_RESPONSE['data'][0],
            {
                **WIREGUARD_PEERS_LIST_RESPONSE['data'][0],
                'id': 'peer2',
                'route_allowed_ips': '0',
            },
        ],
    }

    mock_endpoint('put', '/wireguard/wg0/peers/config', bulk_response)
    mock_endpoint(
        'delete',
        '/wireguard/wg0/peers/config',
        WIREGUARD_PEER_BULK_DELETE_RESPONSE,
        include_login=False,
    )

    endpoint = mock_client.wireguard.peers.config('wg0')

    payload1 = WireguardPeerUpdateItemPayload(id='peer1')
    payload1.public_key = 'p' * 44
    payload1.allowed_ips = ['10.10.0.2/32']

    payload2 = WireguardPeerUpdateItemPayload(id='peer2')
    payload2.public_key = 'q' * 44
    payload2.allowed_ips = ['10.10.0.4/32']

    update_result = endpoint.update_bulk([payload1, payload2])
    delete_result = endpoint.delete_bulk(['peer1', 'peer2'])

    assert len(update_result) == 2
    assert update_result[1].id == 'peer2'
    assert delete_result[0].id == 'peer1'
    assert delete_result[1].id == 'peer2'

    update_body = _request_json_body(1)
    assert update_body['data'][0]['id'] == 'peer1'
    assert update_body['data'][1]['id'] == 'peer2'

    delete_body = _request_json_body(2)
    assert delete_body['data'] == ['peer1', 'peer2']


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_config_api_error_raises(mock_client):
    mock_error_response(
        'get',
        '/wireguard/wg0/peers/config',
        error_code=122,
        error_message='Not found',
        error_source='wireguard',
    )

    endpoint = mock_client.wireguard.peers.config('wg0')
    with pytest.raises(TeltonikaApiException):
        endpoint.get_config()
