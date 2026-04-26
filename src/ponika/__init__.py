from contextlib import ExitStack
import os
import urllib3

from typing import Type, Optional, Dict, Any
from requests import Response, Session
from logging import Logger, getLogger
from ponika.endpoints.auto_reboot import AutoRebootEndpoint
from ponika.endpoints.backup import BackupEndpoint
from ponika.endpoints.data_usage import DataUsageEndpoint
from ponika.endpoints.firmware import FirmwareEndpoint
from ponika.endpoints.users import UsersEndpoint
from ponika.exceptions import TeltonikaApiException, TeltonikaLoginException
from pydantic import ValidationError, validate_call
from time import time

from ponika.endpoints.dhcp import DHCPEndpoint
from ponika.endpoints.gps import GpsEndpoint
from ponika.endpoints.internet_connection import InternetConnectionEndpoint
from ponika.endpoints.ip_neighbors import IpNeighborsEndpoint
from ponika.endpoints.ip_routes import IPRouteEndpoint
from ponika.endpoints.messages import MessagesEndpoint
from ponika.endpoints.modems import ModemsEndpoint
from ponika.endpoints.session import SessionEndpoint
from ponika.endpoints.sms_utilities import SmsUtilitiesEndpoint
from ponika.endpoints.tailscale import TailscaleEndpoint
from ponika.endpoints.unauthorized import UnauthorizedEndpoint
from ponika.endpoints.wireguard import WireguardEndpoint
from ponika.endpoints.wireless import WirelessEndpoint
from ponika.endpoints.zerotier import ZerotierEndpoint
from ponika.models import T, ApiResponse, BasePayload, Token, BaseModel

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ClientConfig(BaseModel):
    """Configuration for PonikaClient."""

    host: str
    username: str
    password: str
    port: Optional[int] = None
    tls: bool = True
    verify_tls: bool = True

    @property
    def resolved_port(self) -> int:
        return self.port or (443 if self.tls else 80)

    @property
    def base_url(self) -> str:
        return f'{"https" if self.tls else "http"}://{self.host}:{self.resolved_port}/api'


class PonikaClient:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int | None = None,
        tls: bool = True,
        verify_tls: bool = True,
    ) -> None:
        self._config = ClientConfig(
            host=host,
            username=username,
            password=password,
            port=port,
            tls=tls,
            verify_tls=verify_tls,
        )

        self._request: Session = Session()
        self._logger: Logger = getLogger(__name__)

        self.auth: None | Token = None

        self.unauthorized = UnauthorizedEndpoint(self)
        self.session = SessionEndpoint(self)
        self.sms_utilities = SmsUtilitiesEndpoint(self)
        self.messages = MessagesEndpoint(self)
        self.gps = GpsEndpoint(self)
        self.backup = BackupEndpoint(self)
        self.auto_reboot = AutoRebootEndpoint(self)
        self.dhcp = DHCPEndpoint(self)
        self.tailscale = TailscaleEndpoint(self)
        self.wireguard = WireguardEndpoint(self)
        self.wireless = WirelessEndpoint(self)
        self.zerotier = ZerotierEndpoint(self)
        self.internet_connection = InternetConnectionEndpoint(self)
        self.ip_routes = IPRouteEndpoint(self)
        self.ip_neighbors = IpNeighborsEndpoint(self)
        self.modems = ModemsEndpoint(self)
        self.firmware = FirmwareEndpoint(self)
        self.users = UsersEndpoint(self)
        self.data_usage = DataUsageEndpoint(self)

    def _get_auth_token(self) -> Optional[str]:
        """Get the current authentication token."""
        if self.auth and self.auth.expires_at > int(time()):
            return self.auth.token

        auth_response = self.login(
            username=self._config.username, password=self._config.password
        )

        self.auth = (
            Token(
                token=auth_response.data.token,
                expires_at=int(time()) + auth_response.data.expires,
            )
            if auth_response.success and auth_response.data
            else None
        )

        if self.auth is None:
            raise TeltonikaLoginException()

        return self.auth.token if self.auth else None

    def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        auth_required: bool = True,
    ) -> object:
        self._logger.info('Making GET request to: %s', endpoint)

        auth_token = self._get_auth_token() if auth_required else None

        response = self._request.get(
            f'{self._config.base_url}{endpoint}',
            verify=self._config.verify_tls,
            params=params,
            headers=(
                {'Authorization': f'Bearer {auth_token}'}
                if auth_token
                else None
            ),
        )

        return response.json()

    def _post_data(
        self,
        endpoint: str,
        data_model: Type[T],
        params: Optional[Dict[str, Any] | BasePayload] = None,
        auth_required: bool = True,
    ) -> ApiResponse[T]:
        if isinstance(params, (BasePayload, BaseModel)):
            params = params.asdict()

        return self._post(
            endpoint=endpoint,
            data_model=data_model,
            params={'data': params},
            auth_required=auth_required,
        )

    def _post(
        self,
        endpoint: str,
        data_model: Type[T],
        params: Optional[Dict[str, Any] | BasePayload] = None,
        auth_required: bool = True,
    ) -> ApiResponse[T]:
        self._logger.info('Making POST request to: %s', endpoint)

        if isinstance(params, (BasePayload, BaseModel)):
            params = params.asdict()

        auth_token = self._get_auth_token() if auth_required else None

        response = self._request.post(
            f'{self._config.base_url}{endpoint}',
            verify=self._config.verify_tls,
            json=params,
            headers=(
                {'Authorization': f'Bearer {auth_token}'}
                if auth_token
                else None
            ),
        )

        try:
            response_obj = ApiResponse[data_model].model_validate(
                response.json()
            )
        except ValidationError as e:
            print(f'Error during request: POST {endpoint}')
            print(
                f'Error during response validation to class ApiResponse[{data_model}]'
            )
            print(f'Response we got: {response.text}')
            raise e

        return response_obj

    def _post_raw(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any] | BasePayload] = None,
        auth_required: bool = True,
    ) -> Response:
        self._logger.info('Making POST request to: %s', endpoint)

        if isinstance(params, (BasePayload, BaseModel)):
            params = params.asdict()

        auth_token = self._get_auth_token() if auth_required else None

        response = self._request.post(
            f'{self._config.base_url}{endpoint}',
            verify=self._config.verify_tls,
            json=params,
            headers=(
                {'Authorization': f'Bearer {auth_token}'}
                if auth_token
                else None
            ),
        )

        return response

    def _post_files(
        self,
        endpoint: str,
        data_model: Type[T],
        files: Optional[Dict[str, str]],
        params: Optional[Dict[str, Any] | BasePayload] = None,
        auth_required: bool = True,
    ) -> ApiResponse[T]:
        self._logger.info('Making POST request to: %s', endpoint)

        if isinstance(params, (BasePayload, BaseModel)):
            params = params.asdict()

        auth_token = self._get_auth_token() if auth_required else None

        files_params = {}

        try:
            with ExitStack() as stack:
                for key, filepath in files.items():
                    filename = os.path.basename(filepath)
                    file_handle = stack.enter_context(open(filepath, 'rb'))

                    files_params[key] = (filename, file_handle)

                files_params = {
                    key: open(filepath, 'rb')
                    for key, filepath in files.items()
                }

                response = self._request.post(
                    f'{self._config.base_url}{endpoint}',
                    verify=self._config.verify_tls,
                    files=files_params,
                    data=params,
                    headers=(
                        {'Authorization': f'Bearer {auth_token}'}
                        if auth_token
                        else None
                    ),
                )
        finally:
            # Dateien immer schließen
            for file_handle in files_params.values():
                file_handle.close()

        return ApiResponse[data_model].model_validate(response.json())

    def _put_data(
        self,
        endpoint: str,
        data_model: Type[T],
        params: Optional[Dict[str, Any] | BasePayload] = None,
        auth_required: bool = True,
    ) -> ApiResponse[T]:
        if isinstance(params, (BasePayload, BaseModel)):
            params = params.asdict()

        return self._put(
            endpoint=endpoint,
            data_model=data_model,
            params={'data': params},
            auth_required=auth_required,
        )

    def _put(
        self,
        endpoint: str,
        data_model: Type[T],
        params: Optional[Dict[str, Any] | BasePayload] = None,
        auth_required: bool = True,
    ) -> ApiResponse[T]:
        self._logger.info('Making POST request to: %s', endpoint)

        if isinstance(params, (BasePayload, BaseModel)):
            params = params.asdict()

        auth_token = self._get_auth_token() if auth_required else None

        response = self._request.put(
            f'{self._config.base_url}{endpoint}',
            verify=self._config.verify_tls,
            json=params,
            headers=(
                {'Authorization': f'Bearer {auth_token}'}
                if auth_token
                else None
            ),
        )

        try:
            response_json = response.json()
        except TypeError:
            raise TeltonikaApiException(
                f'Cannot JSON decode response: {response.text}'
            )

        return ApiResponse[data_model].model_validate(response_json)

    def _delete(
        self,
        endpoint: str,
        data_model: Type[T],
        params: Optional[Dict[str, Any]] = None,
        auth_required: bool = True,
    ) -> ApiResponse[T]:
        self._logger.info('Making POST request to: %s', endpoint)

        auth_token = self._get_auth_token() if auth_required else None

        response = self._request.delete(
            f'{self._config.base_url}{endpoint}',
            verify=self._config.verify_tls,
            json=params,
            headers=(
                {'Authorization': f'Bearer {auth_token}'}
                if auth_token
                else None
            ),
        )

        try:
            response_obj = ApiResponse[data_model].model_validate(
                response.json()
            )
        except ValidationError as e:
            print(f'Error during request: DELETE {endpoint}')
            print(
                f'Error during response validation to class ApiResponse[{data_model}]'
            )
            print(f'Response we got: {response.text}')
            raise e

        return response_obj

    class LoginResponseData(BaseModel):
        """Data model for login response."""

        username: str
        token: str
        expires: int

    @validate_call
    def login(
        self, username: str, password: str
    ) -> ApiResponse[LoginResponseData]:
        """Login to the Ponika API and retrieve a token."""
        self._logger.info('Logging in with username: %s', username)
        response = self._post(
            '/login',
            self.LoginResponseData,
            {'username': username, 'password': password},
            auth_required=False,
        )

        return response

    class LogoutResponseData(BaseModel):
        """Data model for logout response."""

        response: str

    def logout(self) -> ApiResponse[LogoutResponseData]:
        """Logout from the Ponika API."""
        self._logger.info('Logging out...')
        return self._post('/logout', self.LogoutResponseData)
