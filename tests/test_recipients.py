"""Unit tests for recipients endpoints."""

import json

import pytest
import responses

from ponika.endpoints.recipients.email_users import (
    EmailUserCreatePayload,
    EmailUserUpdatePayload,
    EmailTestPayload,
)
from ponika.endpoints.recipients.phone_groups import (
    PhoneGroupCreatePayload,
    PhoneGroupUpdatePayload,
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


PHONE_GROUP_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'group1',
            'name': 'admins',
            'tel': ['+49170123456'],
        }
    ],
}
PHONE_GROUP_SINGLE_RESPONSE = {
    'success': True,
    'data': PHONE_GROUP_LIST_RESPONSE['data'][0],
}
PHONE_GROUP_DELETE_RESPONSE = {'success': True, 'data': {'id': 'group1'}}
PHONE_GROUP_BULK_DELETE_RESPONSE = {
    'success': True,
    'data': [{'id': 'group1'}, {'id': 'group2'}],
}

EMAIL_USER_LIST_RESPONSE = {
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
}
EMAIL_USER_SINGLE_RESPONSE = {
    'success': True,
    'data': EMAIL_USER_LIST_RESPONSE['data'][0],
}
EMAIL_USER_DELETE_RESPONSE = {'success': True, 'data': {'id': 'email1'}}
EMAIL_USER_BULK_DELETE_RESPONSE = {
    'success': True,
    'data': [{'id': 'email1'}, {'id': 'email2'}],
}
TEST_EMAIL_RESPONSE = {'success': True, 'data': {}}


@pytest.mark.unit
@responses.activate
def test_recipients_phone_groups_crud(mock_client):
    mock_endpoint(
        'get', '/recipients/phone_groups/config', PHONE_GROUP_LIST_RESPONSE
    )
    mock_endpoint(
        'get',
        '/recipients/phone_groups/config/group1',
        PHONE_GROUP_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/recipients/phone_groups/config',
        PHONE_GROUP_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/recipients/phone_groups/config/group1',
        PHONE_GROUP_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/recipients/phone_groups/config',
        PHONE_GROUP_LIST_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/recipients/phone_groups/config/group1',
        PHONE_GROUP_DELETE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/recipients/phone_groups/config',
        PHONE_GROUP_BULK_DELETE_RESPONSE,
        include_login=False,
    )

    list_result = mock_client.recipients.phone_groups.get_config()
    single_result = mock_client.recipients.phone_groups.get_config('group1')
    create_result = mock_client.recipients.phone_groups.create(
        PhoneGroupCreatePayload(name='admins', tel=['+49170123456'])
    )
    update_result = mock_client.recipients.phone_groups.update(
        PhoneGroupUpdatePayload(
            id='group1', name='admins', tel=['+49170987654']
        )
    )
    bulk_update_result = mock_client.recipients.phone_groups.update_bulk(
        [PhoneGroupUpdatePayload(id='group1', name='admins')]
    )
    delete_result = mock_client.recipients.phone_groups.delete('group1')
    delete_bulk_result = mock_client.recipients.phone_groups.delete_bulk(
        ['group1', 'group2']
    )

    assert list_result[0].name == 'admins'
    assert single_result.tel == ['+49170123456']
    assert create_result.id == 'group1'
    assert update_result.id == 'group1'
    assert bulk_update_result[0].id == 'group1'
    assert delete_result.id == 'group1'
    assert delete_bulk_result[1].id == 'group2'

    assert _request_json_body(3)['data']['tel'] == ['+49170123456']
    assert 'id' not in _request_json_body(4)['data']
    assert _request_json_body(5)['data'][0]['id'] == 'group1'
    assert _request_json_body(7)['data'] == ['group1', 'group2']


@pytest.mark.unit
@responses.activate
def test_recipients_email_users_crud_and_send_test_email(mock_client):
    mock_endpoint(
        'get', '/recipients/email_users/config', EMAIL_USER_LIST_RESPONSE
    )
    mock_endpoint(
        'get',
        '/recipients/email_users/config/email1',
        EMAIL_USER_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/recipients/email_users/config',
        EMAIL_USER_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/recipients/email_users/config/email1',
        EMAIL_USER_SINGLE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'put',
        '/recipients/email_users/config',
        EMAIL_USER_LIST_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/recipients/email_users/config/email1',
        EMAIL_USER_DELETE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'delete',
        '/recipients/email_users/config',
        EMAIL_USER_BULK_DELETE_RESPONSE,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/recipients/email_users/actions/send_email',
        TEST_EMAIL_RESPONSE,
        include_login=False,
    )

    list_result = mock_client.recipients.email_users.get_config()
    single_result = mock_client.recipients.email_users.get_config('email1')
    create_result = mock_client.recipients.email_users.create(
        EmailUserCreatePayload(
            name='alerts',
            secure_conn=True,
            smtp_ip='smtp.example.com',
            smtp_port='587',
            credentials=True,
            username='alerts',
            password='secret',
            senderemail='alerts@example.com',
            do_not_verify=False,
        )
    )
    update_result = mock_client.recipients.email_users.update(
        EmailUserUpdatePayload(id='email1', name='alerts', secure_conn=False)
    )
    bulk_update_result = mock_client.recipients.email_users.update_bulk(
        [EmailUserUpdatePayload(id='email1', name='alerts')]
    )
    delete_result = mock_client.recipients.email_users.delete('email1')
    delete_bulk_result = mock_client.recipients.email_users.delete_bulk(
        ['email1', 'email2']
    )
    send_result = mock_client.recipients.email_users.send_test_email(
        EmailTestPayload(
            smtp_ip='smtp.example.com',
            smtp_port='587',
            senderemail='alerts@example.com',
            secure_conn=True,
        )
    )

    assert list_result[0].secure_conn is True
    assert list_result[0].do_not_verify is False
    assert single_result.name == 'alerts'
    assert create_result.id == 'email1'
    assert update_result.id == 'email1'
    assert bulk_update_result[0].id == 'email1'
    assert delete_result.id == 'email1'
    assert delete_bulk_result[1].id == 'email2'
    assert send_result is None

    create_body = _request_json_body(3)
    assert create_body['data']['secure_conn'] == '1'
    assert create_body['data']['do_not_verify'] == '0'
    assert 'id' not in _request_json_body(4)['data']
    assert _request_json_body(5)['data'][0]['id'] == 'email1'
    assert _request_json_body(8)['data']['secure_conn'] == '1'


@pytest.mark.unit
@responses.activate
def test_recipients_error_raises(mock_client):
    mock_error_response(
        'get',
        '/recipients/phone_groups/config',
        error_code=122,
        error_message='Not found',
        error_source='recipients',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.recipients.phone_groups.get_config()
