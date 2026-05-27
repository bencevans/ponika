"""Unit tests for firmware endpoints."""

import pytest
import responses

from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


FIRMWARE_STATUS_RESPONSE = {
    'success': True,
    'data': {
        'kernel_version': '5.4.0',
        'version': 'RUT2M_R_00.07.19.2',
        'build_date': '2026-01-01T10:00:00',
    },
}

FIRMWARE_PROGRESS_RESPONSE = {
    'success': True,
    'data': {'percents': '45', 'process': 'downloading'},
}

FIRMWARE_UPDATES_STATUS_RESPONSE = {
    'success': True,
    'data': {
        'device': {
            'version': 'RUT2M_R_00.07.20.0',
            'size': '12345',
            'stable_version': 'RUT2M_R_00.07.19.2',
            'stable_size': '12000',
        }
    },
}

FIRMWARE_VERIFY_RESPONSE = {
    'success': True,
    'data': {
        'valid': '1',
        'hw_support': '1',
        'authorized': '1',
        'passwd_warning': '0',
        'md5': 'abc',
        'size': '123',
        'newer': '1',
        'sha256': 'def',
        'allow_backup': '1',
        'message_code': '0',
        'fw_version': 'RUT2M_R_00.07.20.0',
    },
}

FIRMWARE_DELETE_UPLOAD_RESPONSE = {
    'success': True,
    'data': {'response': 'Deleted'},
}


@pytest.mark.unit
@responses.activate
def test_firmware_device_get_status(mock_client):
    mock_endpoint('get', '/firmware/device/status', FIRMWARE_STATUS_RESPONSE)

    result = mock_client.firmware.device.get_status()

    assert result.version == 'RUT2M_R_00.07.19.2'
    assert result.kernel_version == '5.4.0'


@pytest.mark.unit
@responses.activate
def test_firmware_device_get_progress_status(mock_client):
    mock_endpoint(
        'get',
        '/firmware/device/progress/status',
        FIRMWARE_PROGRESS_RESPONSE,
    )

    result = mock_client.firmware.device.get_progress_status()

    assert result.percents == '45'
    assert result.process == 'downloading'


@pytest.mark.unit
@responses.activate
def test_firmware_device_get_fota_update_status(mock_client):
    mock_endpoint(
        'get',
        '/firmware/device/updates/status',
        FIRMWARE_UPDATES_STATUS_RESPONSE,
    )

    result = mock_client.firmware.device.get_fota_update_status()

    assert result.device.version == 'RUT2M_R_00.07.20.0'


@pytest.mark.unit
@responses.activate
def test_firmware_device_verify_uploaded_firmware(mock_client):
    mock_endpoint('post', '/firmware/actions/verify', FIRMWARE_VERIFY_RESPONSE)

    result = mock_client.firmware.device.verify_uploaded_firmware()

    assert result.valid == '1'
    assert result.fw_version == 'RUT2M_R_00.07.20.0'


@pytest.mark.unit
@responses.activate
def test_firmware_device_delete_uploaded_firmware(mock_client):
    mock_endpoint(
        'post',
        '/firmware/actions/delete_device_firmware',
        FIRMWARE_DELETE_UPLOAD_RESPONSE,
    )

    result = mock_client.firmware.device.delete_uploaded_firmware()

    assert result.response == 'Deleted'


@pytest.mark.unit
@responses.activate
def test_firmware_device_get_status_error_raises(mock_client):
    mock_error_response(
        'get',
        '/firmware/device/status',
        error_code=122,
        error_message='Not found',
        error_source='firmware',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.firmware.device.get_status()
