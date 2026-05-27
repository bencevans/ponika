"""Unit tests for DHCP server endpoints."""

import pytest
import responses

from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


DHCP_V4_CONFIG_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'lan',
            'interface': 'lan',
            'enable_dhcpv4': '1',
            'mode': 'server',
            'start_ip': '192.168.1.100',
            'end_ip': '192.168.1.200',
            'leasetime': '12h',
            'dynamicdhcp': True,
            'force': False,
            'netmask': '255.255.255.0',
            'dhcp_option': [],
            'force_options': False,
        }
    ],
}

DHCP_V4_STATUS_RESPONSE = {
    'success': True,
    'data': [{'id': 'lan', 'running': True, 'interface': ['lan']}],
}

DHCP_V4_LEASES_RESPONSE = {
    'success': True,
    'data': [
        {
            'expires': 123,
            'macaddr': 'AA:BB:CC:DD:EE:FF',
            'ipaddr': '192.168.1.101',
            'hostname': 'test-host',
            'interface': 'lan',
        }
    ],
}


@pytest.mark.unit
@responses.activate
def test_dhcp_ipv4_get_config_list(mock_client):
    mock_endpoint(
        'get', '/dhcp/servers/ipv4/config', DHCP_V4_CONFIG_LIST_RESPONSE
    )

    result = mock_client.dhcp.server_ipv4.get_config()

    assert len(result) == 1
    assert result[0].id == 'lan'
    assert result[0].start_ip == '192.168.1.100'


@pytest.mark.unit
@responses.activate
def test_dhcp_ipv4_get_status(mock_client):
    mock_endpoint('get', '/dhcp/servers/ipv4/status', DHCP_V4_STATUS_RESPONSE)

    result = mock_client.dhcp.server_ipv4.get_status()

    assert len(result) == 1
    assert result[0].id == 'lan'
    assert result[0].running is True


@pytest.mark.unit
@responses.activate
def test_dhcp_ipv4_get_dynamic_leases(mock_client):
    mock_endpoint('get', '/dhcp/leases/ipv4/status', DHCP_V4_LEASES_RESPONSE)

    result = mock_client.dhcp.server_ipv4.get_dynamic_leases()

    assert len(result) == 1
    assert result[0].ipaddr == '192.168.1.101'
    assert result[0].hostname == 'test-host'


@pytest.mark.unit
@responses.activate
def test_dhcp_ipv4_get_config_error_raises(mock_client):
    mock_error_response(
        'get',
        '/dhcp/servers/ipv4/config',
        error_code=122,
        error_message='Not found',
        error_source='dhcp',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.dhcp.server_ipv4.get_config()
