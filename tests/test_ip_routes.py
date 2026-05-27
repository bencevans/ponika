"""Unit tests for IP routes endpoints."""

import pytest
import responses

from ponika.endpoints.ip_routes.ipv4 import (
    Ipv4RouteCreatePayload,
    Ipv4RouteUpdatePayload,
)
from ponika.endpoints.ip_routes.ipv6 import (
    Ipv6RouteCreatePayload,
    Ipv6RouteUpdatePayload,
)
from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


IPV4_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': '1',
            'interface': 'lan',
            'target': '10.10.10.0',
            'netmask': '255.255.255.0',
            'gateway': '192.168.1.1',
            'metric': '10',
        }
    ],
}

IPV4_SINGLE_RESPONSE = {
    'success': True,
    'data': {
        'id': '1',
        'interface': 'lan',
        'target': '10.10.10.0',
        'netmask': '255.255.255.0',
        'gateway': '192.168.1.1',
        'metric': '10',
    },
}

IPV6_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': '1',
            'interface': 'wan',
            'target': '2001:db8::',
            'gateway': 'fe80::1',
            'metric': '20',
        }
    ],
}


@pytest.mark.unit
@responses.activate
def test_ip_routes_ipv4_get_config_list(mock_client):
    mock_endpoint('get', '/ip_routes/ipv4/config', IPV4_LIST_RESPONSE)

    result = mock_client.ip_routes.routes_ipv4.get_config()

    assert len(result) == 1
    assert result[0].id == '1'
    assert result[0].target == '10.10.10.0'


@pytest.mark.unit
@responses.activate
def test_ip_routes_ipv4_get_config_single(mock_client):
    mock_endpoint('get', '/ip_routes/ipv4/config/1', IPV4_SINGLE_RESPONSE)

    result = mock_client.ip_routes.routes_ipv4.get_config('1')

    assert result.id == '1'
    assert result.gateway == '192.168.1.1'


@pytest.mark.unit
@responses.activate
def test_ip_routes_ipv4_create(mock_client):
    mock_endpoint('post', '/ip_routes/ipv4/config', IPV4_SINGLE_RESPONSE)

    payload = Ipv4RouteCreatePayload(
        interface='lan',
        target='10.10.10.0',
        netmask='255.255.255.0',
        gateway='192.168.1.1',
        metric='10',
    )

    result = mock_client.ip_routes.routes_ipv4.create(payload)

    assert result.id == '1'
    assert result.interface == 'lan'


@pytest.mark.unit
@responses.activate
def test_ip_routes_ipv4_update(mock_client):
    mock_endpoint('put', '/ip_routes/ipv4/config/1', IPV4_SINGLE_RESPONSE)

    payload = Ipv4RouteUpdatePayload(
        id='1',
        interface='lan',
        target='10.10.10.0',
        netmask='255.255.255.0',
        gateway='192.168.1.1',
        metric='10',
    )

    result = mock_client.ip_routes.routes_ipv4.update(payload)

    assert result.id == '1'


@pytest.mark.unit
@responses.activate
def test_ip_routes_ipv4_delete(mock_client):
    delete_response = {'success': True, 'data': {'id': '1'}}
    mock_endpoint('delete', '/ip_routes/ipv4/config/1', delete_response)

    result = mock_client.ip_routes.routes_ipv4.delete('1')

    assert result.id == '1'


@pytest.mark.unit
@responses.activate
def test_ip_routes_ipv6_get_config_list(mock_client):
    mock_endpoint('get', '/ip_routes/ipv6/config', IPV6_LIST_RESPONSE)

    result = mock_client.ip_routes.routes_ipv6.get_config()

    assert len(result) == 1
    assert result[0].id == '1'
    assert result[0].target == '2001:db8::'


@pytest.mark.unit
@responses.activate
def test_ip_routes_ipv6_create(mock_client):
    ipv6_single = {'success': True, 'data': IPV6_LIST_RESPONSE['data'][0]}
    mock_endpoint('post', '/ip_routes/ipv6/config', ipv6_single)

    payload = Ipv6RouteCreatePayload(
        interface='wan',
        target='2001:db8::',
        gateway='fe80::1',
        metric='20',
    )

    result = mock_client.ip_routes.routes_ipv6.create(payload)

    assert result.id == '1'


@pytest.mark.unit
@responses.activate
def test_ip_routes_ipv6_update(mock_client):
    ipv6_single = {'success': True, 'data': IPV6_LIST_RESPONSE['data'][0]}
    mock_endpoint('put', '/ip_routes/ipv6/config/1', ipv6_single)

    payload = Ipv6RouteUpdatePayload(
        id='1',
        interface='wan',
        target='2001:db8::',
        gateway='fe80::1',
        metric='20',
    )

    result = mock_client.ip_routes.routes_ipv6.update(payload)

    assert result.id == '1'


@pytest.mark.unit
@responses.activate
def test_ip_routes_ipv4_error_raises(mock_client):
    mock_error_response(
        'get',
        '/ip_routes/ipv4/config',
        error_code=122,
        error_message='Not found',
        error_source='ip_routes',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.ip_routes.routes_ipv4.get_config()
