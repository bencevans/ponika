from typing import Type, Optional, Dict, Any
from requests import Session
from logging import Logger, getLogger
from pydantic import BaseModel, validate_call
from time import time

from ponika.endpoints.dhcp import DhcpEndpoint
from ponika.endpoints.gps import GpsEndpoint
from ponika.endpoints.internet_connection import InternetConnectionEndpoint
from ponika.endpoints.ip_neighbors import IpNeighborsEndpoint
from ponika.endpoints.ip_routes import IpRoutesEndpoint
from ponika.endpoints.messages import MessagesEndpoint
from ponika.endpoints.modems import ModemsEndpoint
from ponika.endpoints.session import SessionEndpoint
from ponika.endpoints.tailscale import TailscaleEndpoint
from ponika.endpoints.unauthorized import UnauthorizedEndpoint
from ponika.endpoints.wireless import WirelessEndpoint
from ponika.models import T, ApiResponse, Token


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
        return (
            f"{'https' if self.tls else 'http'}://{self.host}:{self.resolved_port}/api"
        )


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
        self.messages = MessagesEndpoint(self)
        self.gps = GpsEndpoint(self)
        self.dhcp = DhcpEndpoint(self)
        self.tailscale = TailscaleEndpoint(self)
        self.wireless = WirelessEndpoint(self)
        self.internet_connection = InternetConnectionEndpoint(self)
        self.ip_routes = IpRoutesEndpoint(self)
        self.ip_neighbors = IpNeighborsEndpoint(self)
        self.modems = ModemsEndpoint(self)

    def _get_auth_token(self) -> Optional[str]:
        """Get the current authentication token."""
        if self.auth and self.auth.expires_at > int(time()):
            return self.auth.token

        auth_response = self.login(self._config.username, self._config.password)

        self.auth = (
            Token(
                token=auth_response.data.token,
                expires_at=int(time()) + auth_response.data.expires,
            )
            if auth_response.success and auth_response.data
            else None
        )

        return self.auth.token if self.auth else None

    def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        auth_required: bool = True,
    ) -> object:
        self._logger.info("Making GET request to: %s", endpoint)

        auth_token = self._get_auth_token() if auth_required else None

        response = self._request.get(
            f"{self._config.base_url}{endpoint}",
            verify=self._config.verify_tls,
            params=params,
            headers=({"Authorization": f"Bearer {auth_token}"} if auth_token else None),
        )

        return response.json()

    def _post(
        self,
        endpoint: str,
        data_model: Type[T],
        params: Optional[Dict[str, Any]] = None,
        auth_required: bool = True,
    ) -> ApiResponse[T]:
        self._logger.info("Making POST request to: %s", endpoint)

        auth_token = self._get_auth_token() if auth_required else None

        response = self._request.post(
            f"{self._config.base_url}{endpoint}",
            verify=self._config.verify_tls,
            json=params,
            headers=({"Authorization": f"Bearer {auth_token}"} if auth_token else None),
        )

        return ApiResponse[data_model].model_validate(response.json())

    class LoginResponseData(BaseModel):
        """Data model for login response."""

        username: str
        token: str
        expires: int

    @validate_call
    def login(self, username: str, password: str) -> ApiResponse[LoginResponseData]:
        """Login to the Ponika API and retrieve a token."""
        self._logger.info("Logging in with username: %s", username)
        response = self._post(
            "/login",
            self.LoginResponseData,
            {"username": username, "password": password},
            auth_required=False,
        )

        return response

    class LogoutResponseData(BaseModel):
        """Data model for logout response."""

        response: str

    def logout(self) -> ApiResponse[LogoutResponseData]:
        """Logout from the Ponika API."""
        self._logger.info("Logging out...")
        return self._post("/logout", self.LogoutResponseData)
