"""Unit tests for auto reboot endpoints."""

import json

import pytest
import responses

from ponika.endpoints.auto_reboot.enums import (
    PingWgetAction,
    PingWgetActionWhen,
    PingWgetInterface,
    PingWgetInterval,
    PingWgetIpType,
    PingWgetType,
    SchedulerAction,
    SchedulerMonth,
    SchedulerMonthDay,
    SchedulerPeriod,
    SchedulerWeekDay,
)
from ponika.endpoints.auto_reboot.ping_wget import (
    PingWgetCreatePayload,
    PingWgetUpdatePayload,
)
from ponika.endpoints.auto_reboot.scheduler import (
    SchedulerCreatePayload,
    SchedulerUpdatePayload,
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


SCHEDULER_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'sched1',
            'enable': '1',
            'action': '1',
            'period': 'week',
            'days': ['mon', 'wed'],
            'time': ['03:00:00'],
            'force_last': '0',
        }
    ],
}

SCHEDULER_SINGLE_RESPONSE = {
    'success': True,
    'data': SCHEDULER_LIST_RESPONSE['data'][0],
}

PING_WGET_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'ping1',
            'enable': '1',
            'stop_action': '0',
            'type': 'ping',
            'action': '1',
            'time': '5',
            'retry': '3',
            'time_out': '5',
            'packet_size': '56',
            'interface': '1',
            'ip_type': 'ipv4',
            'ping_port_type': 'ping_port',
            'action_when': 'all',
            'host': ['8.8.8.8'],
            'port_host': '53',
        }
    ],
}

PING_WGET_SINGLE_RESPONSE = {
    'success': True,
    'data': PING_WGET_LIST_RESPONSE['data'][0],
}

PING_WGET_OPTIONS_RESPONSE = {
    'success': True,
    'data': {'available_ports': ['53', '80', '443']},
}


@pytest.mark.unit
@responses.activate
def test_auto_reboot_scheduler_crud_and_bulk(mock_client):
    mock_endpoint(
        'get',
        '/auto_reboot/scheduler/config',
        SCHEDULER_LIST_RESPONSE,
    )
    mock_endpoint(
        'get',
        '/auto_reboot/scheduler/config/sched1',
        SCHEDULER_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/auto_reboot/scheduler/config',
        SCHEDULER_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/auto_reboot/scheduler/config/sched1',
        SCHEDULER_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/auto_reboot/scheduler/config',
        {
            'success': True,
            'data': [
                SCHEDULER_LIST_RESPONSE['data'][0],
                {
                    'id': 'sched2',
                    'enable': '0',
                    'action': '2',
                    'period': 'month',
                    'month_day': ['1'],
                    'months': ['1'],
                    'time': ['04:00:00'],
                    'force_last': '1',
                },
            ],
        },
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/auto_reboot/scheduler/config/sched1',
        {'success': True, 'data': {'id': 'sched1'}},
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/auto_reboot/scheduler/config',
        {'success': True, 'data': [{'id': 'sched1'}, {'id': 'sched2'}]},
        include_login=False,
    )

    list_result = mock_client.auto_reboot.scheduler.get_config()
    single_result = mock_client.auto_reboot.scheduler.get_config('sched1')

    create_result = mock_client.auto_reboot.scheduler.create(
        SchedulerCreatePayload(
            enable=True,
            action=SchedulerAction.DEVICE_REBOOT,
            period=SchedulerPeriod.WEEK,
            days=[SchedulerWeekDay.MONDAY, SchedulerWeekDay.WEDNESDAY],
            time=['03:00:00'],
            force_last=False,
        )
    )
    update_result = mock_client.auto_reboot.scheduler.update(
        SchedulerUpdatePayload(
            id='sched1',
            enable=False,
            action=SchedulerAction.MODEM_REBOOT,
            period=SchedulerPeriod.MONTH,
            month_day=[SchedulerMonthDay.DAY_1],
            months=[SchedulerMonth.JANUARY],
            time=['04:00:00'],
            force_last=True,
        )
    )
    bulk_result = mock_client.auto_reboot.scheduler.update_bulk(
        [
            SchedulerUpdatePayload(
                id='sched1',
                enable=True,
                action=SchedulerAction.DEVICE_REBOOT,
                period=SchedulerPeriod.WEEK,
                days=[SchedulerWeekDay.MONDAY],
                time=['03:00:00'],
            ),
            SchedulerUpdatePayload(
                id='sched2',
                enable=False,
                action=SchedulerAction.MODEM_REBOOT,
                period=SchedulerPeriod.MONTH,
                month_day=[SchedulerMonthDay.DAY_1],
                months=[SchedulerMonth.JANUARY],
                time=['04:00:00'],
                force_last=True,
            ),
        ]
    )
    delete_result = mock_client.auto_reboot.scheduler.delete('sched1')
    delete_bulk_result = mock_client.auto_reboot.scheduler.delete_bulk(
        ['sched1', 'sched2']
    )

    assert len(list_result) == 1
    assert list_result[0].enable is True
    assert list_result[0].action == SchedulerAction.DEVICE_REBOOT
    assert single_result.id == 'sched1'
    assert create_result.id == 'sched1'
    assert update_result.id == 'sched1'
    assert len(bulk_result) == 2
    assert delete_result.id == 'sched1'
    assert delete_bulk_result[1].id == 'sched2'

    create_body = _request_json_body(3)
    assert create_body['data']['enable'] == '1'
    assert create_body['data']['action'] == '1'
    assert create_body['data']['period'] == 'week'

    update_body = _request_json_body(4)
    assert update_body['data']['enable'] == '0'
    assert update_body['data']['action'] == '2'
    assert 'id' not in update_body['data']

    bulk_body = _request_json_body(5)
    assert bulk_body['data'][0]['id'] == 'sched1'
    assert bulk_body['data'][1]['force_last'] == '1'

    delete_bulk_body = _request_json_body(7)
    assert delete_bulk_body['data'] == ['sched1', 'sched2']


@pytest.mark.unit
@responses.activate
def test_auto_reboot_ping_wget_config_and_options(mock_client):
    mock_endpoint(
        'get',
        '/auto_reboot/ping_wget/options',
        PING_WGET_OPTIONS_RESPONSE,
    )
    mock_endpoint(
        'get',
        '/auto_reboot/ping_wget/config',
        PING_WGET_LIST_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'get',
        '/auto_reboot/ping_wget/config/ping1',
        PING_WGET_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/auto_reboot/ping_wget/config',
        PING_WGET_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/auto_reboot/ping_wget/config/ping1',
        PING_WGET_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/auto_reboot/ping_wget/config',
        {
            'success': True,
            'data': [
                PING_WGET_LIST_RESPONSE['data'][0],
                {
                    'id': 'ping2',
                    'enable': '0',
                    'stop_action': '1',
                    'type': 'wget',
                    'action': '3',
                    'time': '15',
                    'interface': '2',
                    'ip_type': 'ipv6',
                    'ping_port_type': 'ping_ip',
                    'action_when': 'any',
                    'host': ['https://example.com'],
                    'port_host': '443',
                },
            ],
        },
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/auto_reboot/ping_wget/config/ping1',
        {'success': True, 'data': {'id': 'ping1'}},
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/auto_reboot/ping_wget/config',
        {'success': True, 'data': [{'id': 'ping1'}, {'id': 'ping2'}]},
        include_login=False,
    )

    list_result = mock_client.auto_reboot.ping_wget.get_config()
    single_result = mock_client.auto_reboot.ping_wget.get_config('ping1')

    create_result = mock_client.auto_reboot.ping_wget.create(
        PingWgetCreatePayload(
            enable=True,
            stop_action=False,
            type=PingWgetType.PING,
            action=PingWgetAction.REBOOT_DEVICE,
            time=PingWgetInterval.MINUTE_5,
            retry='3',
            time_out='5',
            packet_size='56',
            interface=PingWgetInterface.WAN,
            ip_type=PingWgetIpType.IPV4,
            action_when=PingWgetActionWhen.ALL,
            host=['8.8.8.8'],
            port_host='53',
        )
    )
    update_result = mock_client.auto_reboot.ping_wget.update(
        PingWgetUpdatePayload(
            id='ping1',
            enable=False,
            stop_action=True,
            type=PingWgetType.WGET,
            action=PingWgetAction.RESTART_CONNECTION,
            time=PingWgetInterval.MINUTE_15,
            interface=PingWgetInterface.MODEM,
            ip_type=PingWgetIpType.IPV6,
            action_when=PingWgetActionWhen.ANY,
            host=['https://example.com'],
            port_host='443',
        )
    )
    bulk_result = mock_client.auto_reboot.ping_wget.update_bulk(
        [
            PingWgetUpdatePayload(
                id='ping1',
                enable=True,
                type=PingWgetType.PING,
                action=PingWgetAction.REBOOT_DEVICE,
                time=PingWgetInterval.MINUTE_5,
                interface=PingWgetInterface.WAN,
                ip_type=PingWgetIpType.IPV4,
                action_when=PingWgetActionWhen.ALL,
                host=['8.8.8.8'],
                port_host='53',
            ),
            PingWgetUpdatePayload(
                id='ping2',
                enable=False,
                stop_action=True,
                type=PingWgetType.WGET,
                action=PingWgetAction.RESTART_CONNECTION,
                time=PingWgetInterval.MINUTE_15,
                interface=PingWgetInterface.MODEM,
                ip_type=PingWgetIpType.IPV6,
                action_when=PingWgetActionWhen.ANY,
                host=['https://example.com'],
                port_host='443',
            ),
        ]
    )
    delete_result = mock_client.auto_reboot.ping_wget.delete('ping1')
    delete_bulk_result = mock_client.auto_reboot.ping_wget.delete_bulk(
        ['ping1', 'ping2']
    )

    assert len(list_result) == 1
    assert list_result[0].enable is True
    assert list_result[0].type == PingWgetType.PING
    assert single_result.id == 'ping1'
    assert create_result.id == 'ping1'
    assert update_result.id == 'ping1'
    assert len(bulk_result) == 2
    assert delete_result.id == 'ping1'
    assert delete_bulk_result[1].id == 'ping2'

    create_body = _request_json_body(3)
    assert create_body['data']['enable'] == '1'
    assert create_body['data']['stop_action'] == '0'
    assert create_body['data']['type'] == 'ping'

    update_body = _request_json_body(4)
    assert update_body['data']['enable'] == '0'
    assert update_body['data']['stop_action'] == '1'
    assert update_body['data']['action_when'] == 'any'
    assert 'id' not in update_body['data']

    bulk_body = _request_json_body(5)
    assert bulk_body['data'][0]['id'] == 'ping1'
    assert bulk_body['data'][1]['type'] == 'wget'

    delete_bulk_body = _request_json_body(7)
    assert delete_bulk_body['data'] == ['ping1', 'ping2']


@pytest.mark.unit
@responses.activate
def test_auto_reboot_scheduler_error_raises(mock_client):
    mock_error_response(
        'get',
        '/auto_reboot/scheduler/config',
        error_code=122,
        error_message='Not found',
        error_source='auto_reboot',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.auto_reboot.scheduler.get_config()
