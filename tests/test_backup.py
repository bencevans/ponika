"""Unit tests for backup endpoints."""

import json

import pytest
import responses
from pydantic import ValidationError

from ponika.endpoints.backup import (
    BackupEncryptInfoPayload,
    BackupResetSettingsPayload,
    BackupResetType,
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


BACKUP_STATUS_RESPONSE = {
    'success': True,
    'data': {
        'backup_exists': '1',
        'default_exists': '0',
        'sha256': '411c0ef78f6007bf074a8c6bf6b063a4eb6f8b4a1c3edb7285c0e7356e904369',
        'md5': 'fc2a0ae495e6b9645152de5579476aa1',
    },
}

BACKUP_DELETE_RESPONSE = {
    'success': True,
    'data': {
        'sha256': '-',
        'md5': '-',
    },
}

BACKUP_RESET_RESPONSE = {
    'success': True,
    'data': {
        'lan_ip': '192.168.1.1',
        'lan_ipv6': 'fd00::1',
        'http_port': '80',
        'https_port': '443',
    },
}

BACKUP_SUCCESS_NO_DATA = {
    'success': True,
    'data': {},
}
BACKUP_SUCCESS_DATA = {
    'success': True,
    'data': {
        'sha256': '411c0ef78f6007bf074a8c6bf6b063a4eb6f8b4a1c3edb7285c0e7356e904369',
        'md5': 'fc2a0ae495e6b9645152de5579476aa1',
    },
}


@pytest.mark.unit
@responses.activate
def test_backup_get_status(mock_client):
    mock_endpoint('get', '/backup/status', BACKUP_STATUS_RESPONSE)

    result = mock_client.backup.get_status()

    assert result.backup_exists is True
    assert result.default_exists is False
    # fmt: off
    assert result.sha256 == "411c0ef78f6007bf074a8c6bf6b063a4eb6f8b4a1c3edb7285c0e7356e904369"


@pytest.mark.unit
@responses.activate
def test_backup_generate_with_encryption(mock_client):
    mock_endpoint(
        'post',
        '/backup/actions/generate',
        BACKUP_SUCCESS_DATA,
    )

    payload = BackupEncryptInfoPayload(encrypt=True, password='secret')
    result = mock_client.backup.generate(payload)

    assert len(result.sha256) == 64
    assert len(result.md5) == 32


@pytest.mark.unit
@responses.activate
def test_backup_apply_default_payload(mock_client):
    mock_endpoint(
        'post',
        '/backup/actions/apply',
        BACKUP_SUCCESS_NO_DATA,
    )

    mock_client.backup.apply()

    request_body = _request_json_body(1)
    assert request_body['data'] == {'encrypt': '0'}


@pytest.mark.unit
@responses.activate
def test_backup_create_remove_download_and_delete(mock_client):
    mock_endpoint(
        'post',
        '/backup/actions/create_default',
        BACKUP_SUCCESS_NO_DATA,
    )
    mock_endpoint(
        'post',
        '/backup/actions/remove_default',
        BACKUP_SUCCESS_NO_DATA,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/backup/actions/download',
        BACKUP_SUCCESS_NO_DATA,
        include_login=False,
    )
    mock_endpoint(
        'post',
        '/backup/actions/delete',
        BACKUP_DELETE_RESPONSE,
        include_login=False,
    )

    mock_client.backup.create_default()
    mock_client.backup.remove_default()
    mock_client.backup.download()
    result = mock_client.backup.delete()

    assert result.sha256 == '-'
    assert result.md5 == '-'


@pytest.mark.unit
@responses.activate
def test_backup_reset_settings(mock_client):
    mock_endpoint(
        'post',
        '/backup/actions/reset_settings',
        BACKUP_RESET_RESPONSE,
    )

    result = mock_client.backup.reset_settings(
        BackupResetSettingsPayload(type=BackupResetType.USER)
    )

    assert result.lan_ip == '192.168.1.1'
    assert result.https_port == '443'

    request_body = _request_json_body(1)
    assert request_body['data']['type'] == 'user'


@pytest.mark.unit
@responses.activate
def test_backup_upload(mock_client, tmp_path):
    mock_endpoint(
        'post',
        '/backup/actions/upload',
        BACKUP_SUCCESS_NO_DATA,
    )

    backup_file = tmp_path / 'backup.tar.gz'
    backup_file.write_bytes(b'dummy-backup')

    mock_client.backup.upload(str(backup_file))

    upload_call = responses.calls[1].request
    assert (
        upload_call.url == 'https://test-device:443/api/backup/actions/upload'
    )
    assert 'multipart/form-data' in upload_call.headers['Content-Type']


@pytest.mark.unit
def test_backup_encrypt_payload_requires_password():
    with pytest.raises(ValidationError):
        BackupEncryptInfoPayload(encrypt=True)


@pytest.mark.unit
@responses.activate
def test_backup_get_status_error_raises(mock_client):
    mock_error_response(
        'get',
        '/backup/status',
        error_code=122,
        error_message='Not found',
        error_source='backup',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.backup.get_status()


@pytest.mark.unit
@responses.activate
def test_backup_generate_error_raises(mock_client):
    mock_error_response(
        'post',
        '/backup/actions/generate',
        error_code=500,
        error_message='Failed to generate backup',
        error_source='backup',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.backup.generate(BackupEncryptInfoPayload(encrypt=False))
