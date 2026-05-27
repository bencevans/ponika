"""Unit tests for zerotier networks endpoints."""

import json

import pytest
import responses

from ponika.endpoints.zerotier.networks import (
    ZerotierNetworkConfigCreatePayload,
    ZerotierNetworkConfigUpdatePayload,
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


ZEROTIER_NETWORKS_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'net1',
            'enabled': '1',
            'name': 'office',
            'port': '9993',
            'allow_default': '1',
            'allow_global': '0',
            'allow_managed': '1',
            'allow_dns': '1',
            'network_id': 'abcdef1234567890',
            'bridge_to': 'br-lan',
            'custom_planet_file': '/tmp/planet',
            'custom_planet_file:file_size': 100,
        }
    ],
}

ZEROTIER_NETWORKS_SINGLE_RESPONSE = {
    'success': True,
    'data': ZEROTIER_NETWORKS_LIST_RESPONSE['data'][0],
}


@pytest.mark.unit
@responses.activate
def test_zerotier_networks_crud_and_bulk(mock_client):
    base_path = '/zerotier/zt0/networks/config'
    mock_endpoint('get', base_path, ZEROTIER_NETWORKS_LIST_RESPONSE)
    mock_endpoint(
        'get',
        f'{base_path}/net1',
        ZEROTIER_NETWORKS_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'post',
        base_path,
        ZEROTIER_NETWORKS_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        f'{base_path}/net1',
        ZEROTIER_NETWORKS_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        base_path,
        {
            'success': True,
            'data': [
                ZEROTIER_NETWORKS_LIST_RESPONSE['data'][0],
                {
                    **ZEROTIER_NETWORKS_LIST_RESPONSE['data'][0],
                    'id': 'net2',
                    'enabled': '0',
                    'name': 'backup',
                },
            ],
        },
        include_login=False,
    )
    mock_endpoint(
        'delete',
        f'{base_path}/net1',
        {'success': True, 'data': {'id': 'net1'}},
        include_login=False,
    )
    mock_endpoint(
        'delete',
        base_path,
        {'success': True, 'data': [{'id': 'net1'}, {'id': 'net2'}]},
        include_login=False,
    )

    endpoint = mock_client.zerotier.networks.config('zt0')
    list_result = endpoint.get_config()
    single_result = endpoint.get_config('net1')
    create_result = endpoint.create(
        ZerotierNetworkConfigCreatePayload(
            enabled=True,
            name='office',
            allow_default=True,
            allow_global=False,
        )
    )
    update_result = endpoint.update(
        ZerotierNetworkConfigUpdatePayload(
            id='net1',
            enabled=False,
            name='office_new',
            allow_default=False,
            allow_dns=True,
        )
    )
    bulk_result = endpoint.update_bulk(
        [
            ZerotierNetworkConfigUpdatePayload(
                id='net1',
                enabled=True,
                name='office',
                allow_default=True,
            ),
            ZerotierNetworkConfigUpdatePayload(
                id='net2',
                enabled=False,
                name='backup',
                allow_default=False,
            ),
        ]
    )
    delete_result = endpoint.delete('net1')
    delete_bulk_result = endpoint.delete_bulk(['net1', 'net2'])

    assert len(list_result) == 1
    assert list_result[0].enabled is True
    assert list_result[0].allow_global is False
    assert list_result[0].custom_planet_file_file_size == 100
    assert single_result.id == 'net1'
    assert create_result.id == 'net1'
    assert update_result.id == 'net1'
    assert len(bulk_result) == 2
    assert bulk_result[1].id == 'net2'
    assert delete_result.id == 'net1'
    assert delete_bulk_result[1].id == 'net2'

    create_body = _request_json_body(3)
    assert create_body['data']['enabled'] == '1'
    assert create_body['data']['allow_default'] == '1'
    assert create_body['data']['allow_global'] == '0'

    update_body = _request_json_body(4)
    assert 'id' not in update_body['data']
    assert update_body['data']['enabled'] == '0'

    bulk_body = _request_json_body(5)
    assert bulk_body['data'][0]['id'] == 'net1'
    assert bulk_body['data'][1]['enabled'] == '0'


@pytest.mark.unit
@responses.activate
def test_zerotier_networks_error_raises(mock_client):
    mock_error_response(
        'get',
        '/zerotier/zt0/networks/config',
        error_code=122,
        error_message='Not found',
        error_source='zerotier_networks',
    )

    endpoint = mock_client.zerotier.networks.config('zt0')
    with pytest.raises(TeltonikaApiException):
        endpoint.get_config()
