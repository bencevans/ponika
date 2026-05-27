"""Unit tests for message endpoints."""

import json

import pytest
import responses

from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


def _request_json_body(call_index: int) -> dict:
    body = responses.calls[call_index].request.body
    if body is None:
        return {}
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    return json.loads(body)


MESSAGES_STATUS_RESPONSE = {
    'success': True,
    'data': [
        {
            'message': 'Hello from modem',
            'sender': '+49170123456',
            'id': '1001',
            'modem_id': '1-1',
            'status': 'received',
            'date': '2026-02-14 14:10:00',
        }
    ],
}

MESSAGE_SEND_RESPONSE = {
    'success': True,
    'data': {
        'sms_used': 1,
    },
}

MESSAGE_REMOVE_RESPONSE = {
    'success': True,
    'data': {
        'response': 'Messages removed successfully',
    },
}


@pytest.mark.unit
@responses.activate
def test_messages_read(mock_client):
    mock_endpoint('get', '/messages/status', MESSAGES_STATUS_RESPONSE)

    result = mock_client.messages.read()

    assert len(result) == 1
    assert result[0].id == '1001'
    assert result[0].sender == '+49170123456'
    assert result[0].status == 'received'


@pytest.mark.unit
@responses.activate
def test_messages_send(mock_client):
    mock_endpoint('post', '/messages/actions/send', MESSAGE_SEND_RESPONSE)

    result = mock_client.messages.send(
        number='+49170123456',
        message='Test message',
        modem='1-1',
    )

    assert result.sms_used == 1

    request_body = _request_json_body(1)
    assert request_body == {
        'data': {
            'number': '+49170123456',
            'message': 'Test message',
            'modem': '1-1',
        }
    }


@pytest.mark.unit
@responses.activate
def test_messages_post_remove_messages(mock_client):
    mock_endpoint(
        'post',
        '/messages/actions/remove_messages',
        MESSAGE_REMOVE_RESPONSE,
    )

    result = mock_client.messages.remove(
        modem_id='1-1',
        sms_ids=['1001', '1002'],
    )

    assert result.response == 'Messages removed successfully'

    request_body = _request_json_body(1)
    assert request_body == {
        'data': {
            'modem_id': '1-1',
            'sms_id': ['1001', '1002'],
        }
    }


@pytest.mark.unit
@responses.activate
def test_messages_read_error_raises(mock_client):
    mock_error_response(
        'get',
        '/messages/status',
        error_code=122,
        error_message='Not found',
        error_source='messages',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.messages.read()


@pytest.mark.unit
@responses.activate
def test_messages_post_send_error_raises(mock_client):
    mock_error_response(
        'post',
        '/messages/actions/send',
        error_code=400,
        error_message='Invalid modem',
        error_source='messages',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.messages.send(
            number='+49170123456',
            message='Test message',
            modem='invalid-modem',
        )


@pytest.mark.unit
@responses.activate
def test_messages_remove_messages_error_raises(mock_client):
    mock_error_response(
        'post',
        '/messages/actions/remove_messages',
        error_code=400,
        error_message='Invalid sms ids',
        error_source='messages',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.messages.remove(
            modem_id='1-1',
            sms_ids=['invalid'],
        )
