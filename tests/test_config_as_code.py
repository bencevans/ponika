"""Unit tests for declarative config reconciliation."""

import json

import pytest
import responses

from ponika.config import (
    AutoRebootConfig,
    ConfigAction,
    ConfigApplier,
    DhcpConfig,
    IpRoutesConfig,
    PonikaConfig,
    RecipientsConfig,
    SmsUtilitiesConfig,
    WireguardConfig,
    WirelessConfig,
    ZerotierConfig,
)
from ponika.endpoints.recipients.email_users import EmailUserCreatePayload
from ponika.endpoints.recipients.phone_groups import PhoneGroupCreatePayload
from ponika.endpoints.users import UserDefinition
from tests.mocks import mock_endpoint


def _request_json_body(call_index: int) -> dict:
    body = responses.calls[call_index].request.body
    if body is None:
        return {}
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    return json.loads(body)


@pytest.mark.unit
@responses.activate
def test_config_as_code_reconciles_selected_section(mock_client):
    mock_endpoint(
        'get',
        '/recipients/phone_groups/config',
        {
            'success': True,
            'data': [
                {'id': 'keep', 'name': 'Admins', 'tel': ['+49170000000']},
                {'id': 'remove', 'name': 'Old', 'tel': ['+49179999999']},
            ],
        },
    )
    mock_endpoint(
        'put',
        '/recipients/phone_groups/config/keep',
        {
            'success': True,
            'data': {'id': 'keep', 'name': 'Admins', 'tel': ['+49170123456']},
        },
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/recipients/phone_groups/config',
        {
            'success': True,
            'data': {'id': 'new', 'name': 'Ops', 'tel': ['+49170222222']},
        },
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/recipients/phone_groups/config/remove',
        {'success': True, 'data': {'id': 'remove'}},
        include_login=False,
    )

    result = mock_client.config.apply(
        {
            'recipients': {
                'phone_groups': [
                    PhoneGroupCreatePayload(
                        name='Admins', tel=['+49170123456']
                    ),
                    PhoneGroupCreatePayload(name='Ops', tel=['+49170222222']),
                ]
            }
        }
    )

    assert [change.action for change in result.changes] == [
        ConfigAction.UPDATE,
        ConfigAction.CREATE,
        ConfigAction.DELETE,
    ]
    assert _request_json_body(2)['data'] == {
        'name': 'Admins',
        'tel': ['+49170123456'],
    }
    assert _request_json_body(3)['data'] == {
        'name': 'Ops',
        'tel': ['+49170222222'],
    }


@pytest.mark.unit
@responses.activate
def test_config_as_code_compares_only_defined_fields(mock_client):
    mock_endpoint(
        'get',
        '/recipients/email_users/config',
        {
            'success': True,
            'data': [
                {
                    'id': 'email1',
                    'name': 'alerts',
                    'secure_conn': '1',
                    'smtp_ip': 'smtp.example.com',
                    'smtp_port': '587',
                    'credentials': '1',
                    'username': 'alerts',
                    'senderemail': 'alerts@example.com',
                    'do_not_verify': '0',
                    'ca_file': '/etc/certs/ca.pem',
                }
            ],
        },
    )

    result = ConfigApplier(mock_client).apply(
        {
            'recipients': {
                'email_users': [
                    EmailUserCreatePayload(name='alerts', secure_conn=True)
                ]
            }
        }
    )

    assert len(result.unchanged) == 1
    assert result.unchanged[0].match_field == 'name'
    assert len(responses.calls) == 2


@pytest.mark.unit
def test_config_as_code_rejects_unknown_sections(mock_client):
    with pytest.raises(ValueError, match='Unknown config section'):
        mock_client.config.apply({'recipients': {'missing': []}})


@pytest.mark.unit
@responses.activate
def test_config_as_code_accepts_typed_config_model(mock_client):
    mock_endpoint(
        'get',
        '/recipients/phone_groups/config',
        {
            'success': True,
            'data': [{'id': 'group1', 'name': 'Admins'}],
        },
    )

    result = mock_client.config.apply(
        PonikaConfig(
            recipients=RecipientsConfig(
                phone_groups=[PhoneGroupCreatePayload(name='Admins')]
            )
        )
    )

    assert len(result.unchanged) == 1


@pytest.mark.unit
@responses.activate
def test_config_as_code_dry_run_previews_without_writing(mock_client):
    mock_endpoint(
        'get',
        '/recipients/phone_groups/config',
        {
            'success': True,
            'data': [
                {'id': 'keep', 'name': 'Admins', 'tel': ['+49170000000']},
                {'id': 'remove', 'name': 'Old', 'tel': ['+49179999999']},
            ],
        },
    )

    result = mock_client.config.apply(
        PonikaConfig(
            recipients=RecipientsConfig(
                phone_groups=[
                    PhoneGroupCreatePayload(
                        name='Admins', tel=['+49170123456']
                    ),
                    PhoneGroupCreatePayload(name='Ops', tel=['+49170222222']),
                ]
            )
        ),
        dry_run=True,
    )

    assert [change.action for change in result.changes] == [
        ConfigAction.UPDATE,
        ConfigAction.CREATE,
        ConfigAction.DELETE,
    ]
    assert len(responses.calls) == 2
    assert result.updated[0].existing == {
        'id': 'keep',
        'name': 'Admins',
        'tel': ['+49170000000'],
    }
    assert result.updated[0].desired == {
        'id': 'keep',
        'name': 'Admins',
        'tel': ['+49170123456'],
    }
    assert result.created[0].desired == {
        'name': 'Ops',
        'tel': ['+49170222222'],
    }
    assert result.deleted[0].existing == {
        'id': 'remove',
        'name': 'Old',
        'tel': ['+49179999999'],
    }


@pytest.mark.unit
@responses.activate
def test_config_as_code_users_match_by_username(mock_client):
    mock_endpoint(
        'get',
        '/users/config',
        {
            'success': True,
            'data': [
                {
                    'id': 'user1',
                    'username': 'operator',
                    'group': 'user',
                    'ssh_enable': '0',
                }
            ],
        },
    )
    mock_endpoint(
        'put',
        '/users/config/user1',
        {
            'success': True,
            'data': {
                'id': 'user1',
                'username': 'operator',
                'group': 'admin',
                'ssh_enable': '1',
            },
        },
        include_login=False,
    )

    result = mock_client.config.apply(
        {
            'users': [
                UserDefinition(
                    username='operator',
                    password='secret',
                    group='admin',
                    ssh_enable=True,
                )
            ]
        }
    )

    assert len(result.updated) == 1
    assert result.updated[0].match_field == 'username'
    assert result.updated[0].match_value == 'operator'


@pytest.mark.unit
@responses.activate
def test_config_as_code_can_keep_unmanaged_entities(mock_client):
    mock_endpoint(
        'get',
        '/recipients/phone_groups/config',
        {
            'success': True,
            'data': [
                {'id': 'keep', 'name': 'Admins', 'tel': ['+49170123456']},
                {'id': 'unmanaged', 'name': 'Old', 'tel': ['+49179999999']},
            ],
        },
    )

    result = mock_client.config.apply(
        PonikaConfig(
            recipients=RecipientsConfig(
                phone_groups=[
                    PhoneGroupCreatePayload(
                        name='Admins', tel=['+49170123456']
                    ),
                ]
            )
        ),
        delete_unmanaged=False,
    )

    assert len(result.unchanged) == 1
    assert len(result.deleted) == 0
    assert len(responses.calls) == 2


@pytest.mark.unit
def test_config_as_code_typed_models_cover_configurable_endpoints():
    assert set(PonikaConfig.model_fields) == {
        'auto_reboot',
        'dhcp',
        'ip_routes',
        'recipients',
        'sms_utilities',
        'wireguard',
        'wireless',
        'zerotier',
    }
    assert set(AutoRebootConfig.model_fields) == {'scheduler', 'ping_wget'}
    assert set(DhcpConfig.model_fields) == {
        'static_leases_ipv4',
        'static_leases_ipv6',
    }
    assert set(IpRoutesConfig.model_fields) == {'routes_ipv4', 'routes_ipv6'}
    assert set(RecipientsConfig.model_fields) == {
        'phone_groups',
        'email_users',
    }
    assert set(SmsUtilitiesConfig.model_fields) == {'rules'}
    assert set(WireguardConfig.model_fields) == {'config', 'peers'}
    assert set(WirelessConfig.model_fields) == {'interfaces'}
    assert set(ZerotierConfig.model_fields) == {'config', 'networks'}
