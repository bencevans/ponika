"""Unit tests for DHCP static leases endpoints."""

import json

import pytest
import responses

from ponika.endpoints.dhcp.static_leases_ipv4 import (
    StaticLeaseIpv4CreatePayload,
    StaticLeaseIpv4UpdatePayload,
)
from ponika.endpoints.dhcp.static_leases_ipv6 import (
    StaticLeaseIpv6CreatePayload,
    StaticLeaseIpv6UpdatePayload,
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


IPV4_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'lease1',
            'name': 'example1.com',
            'mac': 'AA:BB:CC:DD:EE:FF',
            'ip': '192.168.1.10',
        }
    ],
}

IPV4_SINGLE_RESPONSE = {
    'success': True,
    'data': IPV4_LIST_RESPONSE['data'][0],
}

IPV4_DELETE_RESPONSE = {
    'success': True,
    'data': {'id': 'lease1'},
}

IPV6_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'leasev6_1',
            'name': 'example2.com',
            'duid': '00:01:00:01:2A:1B:3C:4D',
            'hostid': '0001',
        }
    ],
}

IPV6_SINGLE_RESPONSE = {
    'success': True,
    'data': IPV6_LIST_RESPONSE['data'][0],
}

IPV6_DELETE_RESPONSE = {
    'success': True,
    'data': {'id': 'leasev6_1'},
}


@pytest.mark.unit
@responses.activate
def test_static_leases_ipv4_get_list(mock_client):
    mock_endpoint('get', '/dhcp/static_leases/ipv4/config', IPV4_LIST_RESPONSE)

    result = mock_client.dhcp.static_leases_ipv4.get_config()

    assert len(result) == 1
    assert result[0].id == 'lease1'
    assert result[0].mac == 'AA:BB:CC:DD:EE:FF'


@pytest.mark.unit
@responses.activate
def test_static_leases_ipv4_get_single(mock_client):
    mock_endpoint(
        'get',
        '/dhcp/static_leases/ipv4/config/lease1',
        IPV4_SINGLE_RESPONSE,
    )

    result = mock_client.dhcp.static_leases_ipv4.get_config('lease1')

    assert result.id == 'lease1'
    assert result.ip == '192.168.1.10'


@pytest.mark.unit
@responses.activate
def test_static_leases_ipv4_create(mock_client):
    mock_endpoint(
        'post',
        '/dhcp/static_leases/ipv4/config',
        IPV4_SINGLE_RESPONSE,
    )

    payload = StaticLeaseIpv4CreatePayload()
    payload.name = 'device1.example.com'
    payload.mac = 'AA:BB:CC:DD:EE:FF'
    payload.ip = '192.168.1.10'
    result = mock_client.dhcp.static_leases_ipv4.create(payload)

    assert result.id == 'lease1'

    request_body = _request_json_body(1)
    assert request_body['data']['name'] == 'device1.example.com'
    assert request_body['data']['ip'] == '192.168.1.10'


@pytest.mark.unit
@responses.activate
def test_static_leases_ipv4_update(mock_client):
    mock_endpoint(
        'put',
        '/dhcp/static_leases/ipv4/config/lease1',
        IPV4_SINGLE_RESPONSE,
    )

    payload = StaticLeaseIpv4UpdatePayload(id='lease1')
    payload.name = 'example.com'
    payload.mac = 'AA:BB:CC:DD:EE:FF'
    payload.ip = '192.168.1.20'
    result = mock_client.dhcp.static_leases_ipv4.update(payload)

    assert result.id == 'lease1'

    request_body = _request_json_body(1)
    assert 'id' not in request_body['data']
    assert request_body['data']['ip'] == '192.168.1.20'


@pytest.mark.unit
@responses.activate
def test_static_leases_ipv4_update_bulk(mock_client):
    bulk_response = {
        'success': True,
        'data': [
            IPV4_LIST_RESPONSE['data'][0],
            {
                'id': 'lease2',
                'name': 'nas',
                'mac': '11:22:33:44:55:66',
                'ip': '192.168.1.11',
            },
        ],
    }
    mock_endpoint('put', '/dhcp/static_leases/ipv4/config', bulk_response)

    payloads = [
        StaticLeaseIpv4UpdatePayload(id='lease1'),
        StaticLeaseIpv4UpdatePayload(id='lease2'),
    ]
    payloads[0].name = 'OfficePrinter'
    payloads[0].mac = 'AA:BB:CC:DD:EE:FF'
    payloads[0].ip = '192.168.1.10'
    payloads[1].name = 'NAS'
    payloads[1].mac = '11:22:33:44:55:66'
    payloads[1].ip = '192.168.1.11'
    result = mock_client.dhcp.static_leases_ipv4.update_bulk(payloads)

    assert len(result) == 2
    assert result[1].id == 'lease2'

    request_body = _request_json_body(1)
    assert request_body['data'][0]['id'] == 'lease1'
    assert request_body['data'][1]['ip'] == '192.168.1.11'


@pytest.mark.unit
@responses.activate
def test_static_leases_ipv4_delete_and_delete_bulk(mock_client):
    mock_endpoint(
        'delete',
        '/dhcp/static_leases/ipv4/config/lease1',
        IPV4_DELETE_RESPONSE,
    )
    mock_endpoint(
        'delete',
        '/dhcp/static_leases/ipv4/config',
        {
            'success': True,
            'data': [{'id': 'lease1'}, {'id': 'lease2'}],
        },
        include_login=False,
    )

    single = mock_client.dhcp.static_leases_ipv4.delete('lease1')
    bulk_ids = ['lease1', 'lease2']
    bulk = mock_client.dhcp.static_leases_ipv4.delete_bulk(bulk_ids)

    assert single.id == 'lease1'
    assert bulk[1].id == 'lease2'

    request_body = _request_json_body(call_index=2)
    assert request_body['data'] == ['lease1', 'lease2']


@pytest.mark.unit
@responses.activate
def test_static_leases_ipv6_crud_and_bulk(mock_client):
    mock_endpoint(
        'get',
        '/dhcp/static_leases/ipv6/config',
        IPV6_LIST_RESPONSE,
    )
    mock_endpoint(
        'get',
        '/dhcp/static_leases/ipv6/config/leasev6_1',
        IPV6_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/dhcp/static_leases/ipv6/config',
        IPV6_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/dhcp/static_leases/ipv6/config/leasev6_1',
        IPV6_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/dhcp/static_leases/ipv6/config',
        {
            'success': True,
            'data': [
                IPV6_LIST_RESPONSE['data'][0],
                {
                    'id': 'leasev6_2',
                    'name': 'example3.com',
                    'duid': '00:01:00:01:AA:BB:CC:DD',
                    'hostid': '0002',
                },
            ],
        },
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/dhcp/static_leases/ipv6/config/leasev6_1',
        IPV6_DELETE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/dhcp/static_leases/ipv6/config',
        {
            'success': True,
            'data': [{'id': 'leasev6_1'}, {'id': 'leasev6_2'}],
        },
        include_login=False,
    )

    list_result = mock_client.dhcp.static_leases_ipv6.get_config()
    single_result = mock_client.dhcp.static_leases_ipv6.get_config('leasev6_1')
    create_payload = StaticLeaseIpv6CreatePayload()
    create_payload.name = 'example1.com'
    create_payload.duid = '00:01:00:01:2A:1B:3C:4D'
    create_payload.hostid = '0001'
    create_result = mock_client.dhcp.static_leases_ipv6.create(create_payload)

    update_payload = StaticLeaseIpv6UpdatePayload(id='leasev6_1')
    update_payload.name = 'example2.com'
    update_payload.duid = '00:01:00:01:2A:1B:3C:4D'
    update_payload.hostid = '000A'
    update_result = mock_client.dhcp.static_leases_ipv6.update(update_payload)

    bulk_payload_1 = StaticLeaseIpv6UpdatePayload(id='leasev6_1')
    bulk_payload_1.name = 'exampl3.com'
    bulk_payload_1.duid = '00:01:00:01:2A:1B:3C:4D'
    bulk_payload_1.hostid = '0001'

    bulk_payload_2 = StaticLeaseIpv6UpdatePayload(id='leasev6_2')
    bulk_payload_2.name = 'example4.com'
    bulk_payload_2.duid = '00:01:00:01:AA:BB:CC:DD'
    bulk_payload_2.hostid = '0002'

    bulk_result = mock_client.dhcp.static_leases_ipv6.update_bulk(
        [bulk_payload_1, bulk_payload_2]
    )
    delete_result = mock_client.dhcp.static_leases_ipv6.delete('leasev6_1')
    delete_bulk_result = mock_client.dhcp.static_leases_ipv6.delete_bulk(
        ['leasev6_1', 'leasev6_2']
    )

    assert len(list_result) == 1
    assert single_result.id == 'leasev6_1'
    assert create_result.id == 'leasev6_1'
    assert update_result.id == 'leasev6_1'
    assert len(bulk_result) == 2
    assert delete_result.id == 'leasev6_1'
    assert delete_bulk_result[1].id == 'leasev6_2'

    create_body = _request_json_body(3)
    assert create_body['data']['hostid'] == '0001'

    update_body = _request_json_body(4)
    assert 'id' not in update_body['data']

    bulk_update_body = _request_json_body(5)
    assert bulk_update_body['data'][0]['id'] == 'leasev6_1'

    bulk_delete_body = _request_json_body(7)
    assert bulk_delete_body['data'] == ['leasev6_1', 'leasev6_2']


@pytest.mark.unit
@responses.activate
def test_static_leases_error_raises(mock_client):
    mock_error_response(
        'get',
        '/dhcp/static_leases/ipv4/config',
        error_code=122,
        error_message='Not found',
        error_source='dhcp',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.dhcp.static_leases_ipv4.get_config()
