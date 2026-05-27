"""Unit tests for users endpoints."""

import pytest
import responses

from ponika.exceptions import TeltonikaApiException
from ponika.endpoints.users import UserDefinition, UserUpdateDefinition
from tests.mocks import mock_endpoint, mock_error_response


USERS_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': '1',
            'username': 'admin2',
            'group': 'admin',
            'ssh_enable': True,
        }
    ],
}

USER_SINGLE_RESPONSE = {
    'success': True,
    'data': {
        'id': '1',
        'username': 'admin2',
        'group': 'admin',
        'ssh_enable': True,
    },
}

USER_DELETE_RESPONSE = {
    'success': True,
    'data': {'id': '1'},
}


@pytest.mark.unit
@responses.activate
def test_users_get_config_list(mock_client):
    mock_endpoint('get', '/users/config', USERS_LIST_RESPONSE)

    result = mock_client.users.get_config()

    assert len(result) == 1
    assert result[0].id == '1'
    assert result[0].username == 'admin2'


@pytest.mark.unit
@responses.activate
def test_users_get_config_single(mock_client):
    mock_endpoint('get', '/users/config/1', USER_SINGLE_RESPONSE)

    result = mock_client.users.get_config('1')

    assert result.id == '1'
    assert result.group == 'admin'
    assert result.ssh_enable is True


@pytest.mark.unit
@responses.activate
def test_users_create(mock_client):
    mock_endpoint('post', '/users/config', USER_SINGLE_RESPONSE)

    payload = UserDefinition(
        username='admin2',
        password='secret',
        group='admin',
        ssh_enable=True,
    )

    result = mock_client.users.create(payload)

    assert result.id == '1'
    assert result.username == 'admin2'


@pytest.mark.unit
@responses.activate
def test_users_update(mock_client):
    mock_endpoint('put', '/users/config/1', USER_SINGLE_RESPONSE)

    payload = UserUpdateDefinition(id='1', group='admin', ssh_enable=True)
    result = mock_client.users.update(payload)

    assert result.id == '1'
    assert result.ssh_enable is True


@pytest.mark.unit
@responses.activate
def test_users_delete(mock_client):
    mock_endpoint('delete', '/users/config/1', USER_DELETE_RESPONSE)

    result = mock_client.users.delete('1')

    assert result.id == '1'


@pytest.mark.unit
@responses.activate
def test_users_get_config_error_raises(mock_client):
    mock_error_response(
        'get',
        '/users/config',
        error_code=122,
        error_message='Not found',
        error_source='users',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.users.get_config()
