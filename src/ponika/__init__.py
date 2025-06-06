from typing import Type, Optional, Dict, Any
from requests import Session
from logging import Logger, getLogger
from pydantic import BaseModel, validate_call
from time import time

from ponika.endpoints.dhcp import DhcpEndpoint
from ponika.endpoints.gps import GpsEndpoint
from ponika.endpoints.internet_connection import InternetConnectionEndpoint
from ponika.endpoints.messages import MessagesEndpoint
from ponika.endpoints.session import SessionEndpoint
from ponika.endpoints.tailscale import TailscaleEndpoint
from ponika.endpoints.unauthorized import UnauthorizedEndpoint
from ponika.endpoints.wireless import WirelessEndpoint
from ponika.models import T, ApiResponse, Token


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
        self.username = username
        self.password = password
        self.host = host
        self.port = port or (443 if tls else 80)
        self.tls = tls
        self.verify_tls = verify_tls
        self.base_url = f"{'https' if tls else 'http'}://{self.host}:{self.port}/api"

        self.request: Session = Session()
        self.logger: Logger = getLogger(__name__)

        self.auth: None | Token = None

        self.unauthorized = UnauthorizedEndpoint(self)
        self.session = SessionEndpoint(self)
        self.messages = MessagesEndpoint(self)
        self.gps = GpsEndpoint(self)
        self.dhcp = DhcpEndpoint(self)
        self.tailscale = TailscaleEndpoint(self)
        self.wireless = WirelessEndpoint(self)
        self.internet_connection = InternetConnectionEndpoint(self)

    def get_auth_token(self) -> Optional[str]:
        """Get the current authentication token."""
        if self.auth and self.auth.expires_at > int(time()):
            return self.auth.token

        auth_response = self.login(self.username, self.password)

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
        self.logger.info("Making GET request to: %s", endpoint)

        auth_token = self.get_auth_token() if auth_required else None

        response = self.request.get(
            f"{self.base_url}{endpoint}",
            verify=self.verify_tls,
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
        self.logger.info("Making POST request to: %s", endpoint)

        auth_token = self.get_auth_token() if auth_required else None

        response = self.request.post(
            f"{self.base_url}{endpoint}",
            verify=self.verify_tls,
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
        self.logger.info("Logging in with username: %s", username)
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
        self.logger.info("Logging out...")
        return self._post("/logout", self.LogoutResponseData)
