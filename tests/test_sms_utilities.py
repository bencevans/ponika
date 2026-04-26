"""Unit tests for sms utilities rules endpoints."""

import json

import pytest
import responses

from ponika.endpoints.sms_utilities.enums import (
    DeviceParamType,
    SmsRuleAction,
    SmsRuleAllowedPhone,
    SmsRuleAuthorization,
)
from ponika.endpoints.sms_utilities.rules import (
    SmsRuleCreatePayload,
    SmsRuleUpdatePayload,
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


SMS_RULES_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'rule1',
            'enabled': '1',
            'action': 'send_status',
            'smstext': 'status',
            'respond': '1',
            'authorization': 'password',
            'allowed_phone': 'all',
            'password:set': '1',
        }
    ],
}

SMS_RULES_SINGLE_RESPONSE = {
    'success': True,
    'data': SMS_RULES_LIST_RESPONSE['data'][0],
}

SMS_RULES_DELETE_RESPONSE = {
    'success': True,
    'data': {'id': 'rule1'},
}

SMS_RULES_BULK_DELETE_RESPONSE = {
    'success': True,
    'data': [{'id': 'rule1'}, {'id': 'rule2'}],
}

SMS_RULES_OPTIONS_RESPONSE = {
    'success': True,
    'data': {
        'actions': ['reboot', 'send_status'],
        'params': [
            {
                'type': 'io',
                'description': 'Relay output',
                'io_name': 'Relay',
                'block_pins': [5, 10],
                'id': 'g7',
            }
        ],
    },
}


@pytest.mark.unit
@responses.activate
def test_sms_utilities_rules_crud_and_options(mock_client):
    mock_endpoint(
        'get', '/sms_utilities/rules/options', SMS_RULES_OPTIONS_RESPONSE
    )
    mock_endpoint(
        'get',
        '/sms_utilities/rules/config',
        SMS_RULES_LIST_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'get',
        '/sms_utilities/rules/config/rule1',
        SMS_RULES_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/sms_utilities/rules/config',
        SMS_RULES_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/sms_utilities/rules/config/rule1',
        SMS_RULES_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/sms_utilities/rules/config/rule1',
        SMS_RULES_DELETE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/sms_utilities/rules/config',
        SMS_RULES_BULK_DELETE_RESPONSE,
        include_login=False,
    )

    options = mock_client.sms_utilities.rules.get_options()
    list_result = mock_client.sms_utilities.rules.get_config()
    single_result = mock_client.sms_utilities.rules.get_config('rule1')
    create_result = mock_client.sms_utilities.rules.create(
        SmsRuleCreatePayload(
            enabled=True,
            action=SmsRuleAction.SEND_STATUS,
            smstext='status',
            respond=True,
            authorization=SmsRuleAuthorization.PASSWORD,
            allowed_phone=SmsRuleAllowedPhone.ALL,
        )
    )
    update_result = mock_client.sms_utilities.rules.update(
        SmsRuleUpdatePayload(
            id='rule1',
            enabled=False,
            action=SmsRuleAction.REBOOT,
            smstext='reboot',
            authorization=SmsRuleAuthorization.LOCAL,
            password='secret123',
            allowed_phone=SmsRuleAllowedPhone.SINGLE,
            tel='+49170123456',
        )
    )
    delete_result = mock_client.sms_utilities.rules.delete('rule1')
    delete_bulk_result = mock_client.sms_utilities.rules.delete_bulk(
        ['rule1', 'rule2']
    )

    assert options.actions[0] == SmsRuleAction.REBOOT
    assert options.params[0].type == DeviceParamType.IO

    assert len(list_result) == 1
    assert list_result[0].enabled is True
    assert list_result[0].password_set is True
    assert single_result.id == 'rule1'

    assert create_result.id == 'rule1'
    assert update_result.id == 'rule1'
    assert delete_result.id == 'rule1'
    assert delete_bulk_result[1].id == 'rule2'

    create_body = _request_json_body(4)
    assert create_body['data']['enabled'] == '1'
    assert create_body['data']['action'] == 'send_status'

    update_body = _request_json_body(5)
    assert update_body['data']['enabled'] == '0'
    assert update_body['data']['authorization'] == 'local'
    assert update_body['data']['allowed_phone'] == 'single'
    assert 'id' not in update_body['data']

    delete_bulk_body = _request_json_body(7)
    assert delete_bulk_body['data'] == ['rule1', 'rule2']


@pytest.mark.unit
@responses.activate
def test_sms_utilities_rules_error_raises(mock_client):
    mock_error_response(
        'get',
        '/sms_utilities/rules/config',
        error_code=122,
        error_message='Not found',
        error_source='sms_utilities',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.sms_utilities.rules.get_config()
