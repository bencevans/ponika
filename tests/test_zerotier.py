"""Unit tests for zerotier config endpoints."""

import json

import pytest
import responses

from ponika.endpoints.zerotier.config import (
    ZerotierConfigCreatePayload,
    ZerotierConfigUpdatePayload,
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


ZEROTIER_CONFIG_LIST_RESPONSE = {
    'success': True,
    'data': [{'id': 'zt0', 'enabled': '1', 'name': 'zerotier_main'}],
}

ZEROTIER_CONFIG_SINGLE_RESPONSE = {
    'success': True,
    'data': ZEROTIER_CONFIG_LIST_RESPONSE['data'][0],
}


@pytest.mark.unit
@responses.activate
def test_zerotier_config_crud_and_bulk(mock_client):
    mock_endpoint('get', '/zerotier/config', ZEROTIER_CONFIG_LIST_RESPONSE)
    mock_endpoint(
        'get',
        '/zerotier/config/zt0',
        ZEROTIER_CONFIG_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/zerotier/config',
        ZEROTIER_CONFIG_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/zerotier/config/zt0',
        ZEROTIER_CONFIG_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/zerotier/config',
        {
            'success': True,
            'data': [
                ZEROTIER_CONFIG_LIST_RESPONSE['data'][0],
                {'id': 'zt1', 'enabled': '0', 'name': 'zerotier_backup'},
            ],
        },
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/zerotier/config/zt0',
        {'success': True, 'data': {'id': 'zt0'}},
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/zerotier/config',
        {'success': True, 'data': [{'id': 'zt0'}, {'id': 'zt1'}]},
        include_login=False,
    )

    list_result = mock_client.zerotier.config.get_config()
    single_result = mock_client.zerotier.config.get_config('zt0')

    create_result = mock_client.zerotier.config.create(
        ZerotierConfigCreatePayload(enabled=True, name='zerotier_main')
    )
    update_result = mock_client.zerotier.config.update(
        ZerotierConfigUpdatePayload(
            id='zt0', enabled=False, name='zerotier_renamed'
        )
    )
    bulk_result = mock_client.zerotier.config.update_bulk(
        [
            ZerotierConfigUpdatePayload(
                id='zt0', enabled=True, name='zerotier_main'
            ),
            ZerotierConfigUpdatePayload(
                id='zt1', enabled=False, name='zerotier_backup'
            ),
        ]
    )
    delete_result = mock_client.zerotier.config.delete('zt0')
    delete_bulk_result = mock_client.zerotier.config.delete_bulk(
        ['zt0', 'zt1']
    )

    assert len(list_result) == 1
    assert list_result[0].enabled is True
    assert single_result.id == 'zt0'
    assert create_result.id == 'zt0'
    assert update_result.id == 'zt0'
    assert len(bulk_result) == 2
    assert bulk_result[1].id == 'zt1'
    assert delete_result.id == 'zt0'
    assert delete_bulk_result[1].id == 'zt1'

    create_body = _request_json_body(3)
    assert create_body['data']['enabled'] == '1'

    update_body = _request_json_body(4)
    assert 'id' not in update_body['data']
    assert update_body['data']['enabled'] == '0'

    bulk_body = _request_json_body(5)
    assert bulk_body['data'][0]['id'] == 'zt0'
    assert bulk_body['data'][1]['enabled'] == '0'

    delete_bulk_body = _request_json_body(7)
    assert delete_bulk_body['data'] == ['zt0', 'zt1']


@pytest.mark.unit
@responses.activate
def test_zerotier_config_error_raises(mock_client):
    mock_error_response(
        'get',
        '/zerotier/config',
        error_code=122,
        error_message='Not found',
        error_source='zerotier',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.zerotier.config.get_config()
