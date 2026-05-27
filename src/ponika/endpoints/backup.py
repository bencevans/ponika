from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import model_validator

from ponika.endpoints import Endpoint
from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel, BasePayload


class BackupEncryptInfoPayload(BasePayload):
    encrypt: bool = False
    password: Optional[str] = None

    @model_validator(mode='after')
    def validate_password_requirement(self) -> 'BackupEncryptInfoPayload':
        if self.encrypt and not self.password:
            raise ValueError('password is required when encrypt is true')
        return self


class BackupResetType(str, Enum):
    SYSTEM = 'system'
    FACTORY = 'factory'
    USER = 'user'


class BackupResetSettingsPayload(BasePayload):
    type: BackupResetType


class BackupHashResponse(BaseModel):
    sha256: str | None = '-'
    md5: str | None = '-'


class BackupActionResponse(BaseModel):
    pass


class BackupResetSettingsResponse(BaseModel):
    lan_ip: Optional[str] = None
    lan_ipv6: Optional[str] = None
    http_port: Optional[str] = None
    https_port: Optional[str] = None


class BackupStatusResponse(BaseModel):
    backup_exists: Optional[bool] = None
    default_exists: Optional[bool] = None
    sha256: Optional[str] = None
    md5: Optional[str] = None


class BackupEndpoint(Endpoint):
    def get_status(self) -> BackupStatusResponse:
        response = ApiResponse[BackupStatusResponse].model_validate(
            self._client._get('/backup/status')
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)
        if response.data is None:
            raise TeltonikaApiException(
                'Missing data in backup status response'
            )

        return response.data

    def generate(
        self,
        payload: Optional[BackupEncryptInfoPayload] = None,
    ) -> BackupHashResponse:
        response = self._client._post_data(
            endpoint='/backup/actions/generate',
            data_model=BackupHashResponse,
            params=payload or BackupEncryptInfoPayload(),
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)
        if response.data is None:
            raise TeltonikaApiException(
                'Missing data in backup generate response'
            )

        return response.data

    def apply(
        self,
        payload: Optional[BackupEncryptInfoPayload] = None,
    ) -> BackupActionResponse:
        response = self._client._post_data(
            endpoint='/backup/actions/apply',
            data_model=BackupActionResponse,
            params=payload or BackupEncryptInfoPayload(),
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)
        if response.data is None:
            raise TeltonikaApiException(
                'Missing data in backup apply response'
            )

        return response.data

    def create_default(self) -> BackupActionResponse:
        response = self._client._post(
            endpoint='/backup/actions/create_default',
            data_model=BackupActionResponse,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)
        if response.data is None:
            raise TeltonikaApiException(
                'Missing data in backup create_default response'
            )

        return response.data

    def remove_default(self) -> BackupActionResponse:
        response = self._client._post(
            endpoint='/backup/actions/remove_default',
            data_model=BackupActionResponse,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)
        if response.data is None:
            raise TeltonikaApiException(
                'Missing data in backup remove_default response'
            )

        return response.data

    def download(self) -> bytes:
        response = self._client._post_raw(endpoint='/backup/actions/download')

        if response.status_code >= 400:
            raise RuntimeError(
                f'Download failed: {response.status_code} {response.text}'
            )

        return response.content

    def download_to_file(self, target: str | Path) -> bool:
        target = Path(target)
        response = self._client._post_raw(endpoint='/backup/actions/download')

        if response.status_code >= 400:
            raise RuntimeError(
                f'Download failed: {response.status_code} {response.text}'
            )

        target.parent.mkdir(parents=True, exist_ok=True)

        with target.open('wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        return True

    def upload(self, file_path: str) -> BackupActionResponse:
        response = self._client._post_files(
            endpoint='/backup/actions/upload',
            data_model=BackupActionResponse,
            files={'file': file_path},
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)
        if response.data is None:
            raise TeltonikaApiException(
                'Missing data in backup upload response'
            )

        return response.data

    def delete(self) -> BackupHashResponse:
        response = self._client._post(
            endpoint='/backup/actions/delete',
            data_model=BackupHashResponse,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)
        if response.data is None:
            raise TeltonikaApiException(
                'Missing data in backup delete response'
            )

        return response.data

    def reset_settings(
        self,
        payload: BackupResetSettingsPayload,
    ) -> BackupResetSettingsResponse:
        response = self._client._post_data(
            endpoint='/backup/actions/reset_settings',
            data_model=BackupResetSettingsResponse,
            params=payload,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)
        if response.data is None:
            raise TeltonikaApiException(
                'Missing data in backup reset settings response'
            )

        return response.data
