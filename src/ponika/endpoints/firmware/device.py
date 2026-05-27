import datetime
from ponika.endpoints import Endpoint
from pydantic import BaseModel

from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse


class FirmwareDeviceStatusResponse(BaseModel):
    kernel_version: str
    version: str
    build_date: datetime.datetime


class FirmwareDeviceProgressStatusResponse(BaseModel):
    percents: str
    process: str


class FirmwareDeviceUploadDeleteResponse(BaseModel):
    response: str


class FirmwareDeviceUploadResponse(BaseModel):
    valid: str
    hw_support: str
    authorized: str
    passwd_warning: str
    md5: str
    size: str
    newer: str
    sha256: str
    allow_backup: str
    message_code: str
    fw_version: str


class FirmwareDeviceFotaUpdateStatusResponse(BaseModel):
    class DeviceFotaUpdateStatus(BaseModel):
        version: str
        size: str
        stable_version: str
        stable_size: str

    device: DeviceFotaUpdateStatus


class FirmwareDeviceEndpoint(Endpoint):
    def get_status(self) -> FirmwareDeviceStatusResponse:
        response = ApiResponse[FirmwareDeviceStatusResponse].model_validate(
            self._client._get('/firmware/device/status')
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data

    def get_progress_status(self) -> FirmwareDeviceProgressStatusResponse:
        response = ApiResponse[
            FirmwareDeviceProgressStatusResponse
        ].model_validate(self._client._get('/firmware/device/progress/status'))

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data

    def get_fota_update_status(self) -> FirmwareDeviceFotaUpdateStatusResponse:
        response = ApiResponse[
            FirmwareDeviceFotaUpdateStatusResponse
        ].model_validate(self._client._get('/firmware/device/updates/status'))

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data

    def download_from_fota(self):
        response = self._client._post(
            endpoint='/firmware/actions/fota_download',
            data_model=None,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data

    def upload_firmware(
        self,
        file_path: str,
        keep_settings: bool = True,
        suppress_validation: bool = False,
    ):
        params = {
            'keep_settings': '1' if keep_settings else '0',
            'suppress_validation': '1' if suppress_validation else '0',
        }

        response = self._client._post_files(
            endpoint='/firmware/actions/upload_device_firmware',
            data_model=FirmwareDeviceUploadResponse,
            files={'file': file_path},
            params=params,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data

    def verify_uploaded_firmware(self) -> FirmwareDeviceUploadResponse:
        response = self._client._post(
            endpoint='/firmware/actions/verify',
            data_model=FirmwareDeviceUploadResponse,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data

    def delete_uploaded_firmware(self) -> FirmwareDeviceUploadDeleteResponse:
        response = self._client._post(
            endpoint='/firmware/actions/delete_device_firmware',
            data_model=FirmwareDeviceUploadDeleteResponse,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data

    def start_firmware_upgrade(
        self, keep_settings: bool = True, suppress_validation: bool = False
    ):
        params = {
            'keep_settings': '1' if keep_settings else '0',
            'suppress_validation': '1' if suppress_validation else '0',
        }

        response = self._client._post_data(
            endpoint='/firmware/actions/upgrade',
            params=params,
            data_model=None,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data
