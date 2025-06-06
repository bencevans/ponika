from typing import Literal, Type, TypeVar, Generic, Optional, Dict, Any
from requests import Session
from logging import Logger, getLogger
from pydantic import BaseModel, validate_call
from time import time

T = TypeVar("T", bound=BaseModel)


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: None | T


class Token(BaseModel):
    """Data model for token response."""

    token: str
    expires_at: int


class PonikaClient:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int = 443,
        use_tls: bool = True,
    ) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.base_url = f"{'https' if use_tls else 'http'}://{host}:{port}/api"

        self.request: Session = Session()
        self.logger: Logger = getLogger(__name__)

        self.auth: None | Token = None

        self.unauthorized = UnauthorizedEndpoint(self)
        self.session = SessionEndpoint(self)
        self.messages = MessagesEndpoint(self)
        self.gps = GpsEndpoint(self)

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
        print(self.auth)

        return self.auth.token if self.auth else None

    def _get(
        self,
        endpoint: str,
        data_model: Type[T],
        params: Optional[Dict[str, Any]] = None,
        auth_required: bool = True,
    ) -> ApiResponse[T]:
        self.logger.info("Making GET request to: %s", endpoint)

        auth_token = self.get_auth_token() if auth_required else None

        response = self.request.get(
            f"{self.base_url}{endpoint}",
            verify=False,
            params=params,
            headers=({"Authorization": f"Bearer {auth_token}"} if auth_token else None),
        )
        print(response.json())
        response.raise_for_status()

        return ApiResponse[data_model].model_validate(response.json())

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
            verify=False,
            json=params,
            headers=({"Authorization": f"Bearer {auth_token}"} if auth_token else None),
        )
        response.raise_for_status()

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


class SessionEndpoint:
    def __init__(self, client: PonikaClient) -> None:
        self.client: PonikaClient = client

    class SessionResponseData(BaseModel):
        """Data model for session response."""

        active: bool

    def get_status(self) -> ApiResponse[SessionResponseData]:
        """Fetch session information from the device."""
        self.client.logger.info("Accessing session endpoint...")
        return self.client._get("/session/status", self.SessionResponseData)


class UnauthorizedEndpoint:
    def __init__(self, client: PonikaClient) -> None:
        self.client: PonikaClient = client

    class UnauthorizedStatusResponseData(BaseModel):
        """Data model for GET /unauthorized/status response."""

        device_name: str
        device_model: str
        device_identifier: str
        api_version: str
        lang: str

    def get_status(self) -> ApiResponse[UnauthorizedStatusResponseData]:
        """Fetch unauthorized status from the device."""
        self.client.logger.info("Accessing unauthorized endpoint...")
        return self.client._get(
            "/unauthorized/status",
            self.UnauthorizedStatusResponseData,
        )


class GpsEndpoint:
    def __init__(self, client: PonikaClient) -> None:
        self.client: PonikaClient = client
        self.position = self.GpsPositionEndpoint(client)

    class GetGlobalResponseData(BaseModel):
        """Data model for GET /gps/global response."""

        enabled: Literal["0", "1"]
        galileo_sup: Literal["0", "1"]
        glonass_sup: Literal["0", "1"]
        beidou_sup: Literal["0", "1"]
        dpo_enabled: Optional[Literal["0", "1"]] = None
        mode: Optional[Literal["0", "1"]] = None
        interval: Optional[str] = None
        timeout: Optional[str] = None

    def get_global(self) -> ApiResponse[GetGlobalResponseData]:
        """Fetch global GPS config."""
        self.client.logger.info("Accessing GPS global endpoint...")
        return self.client._get(
            "/gps/global",
            self.GetGlobalResponseData,
        )

    class GpsStatusResponseData(BaseModel):
        """Data model for GET /gps/status response."""

        dpo_support: bool
        uptime: int

    def get_status(self) -> ApiResponse[GpsStatusResponseData]:
        """Fetch GPS status from the device."""
        self.client.logger.info("Accessing GPS endpoint...")
        return self.client._get(
            "/gps/status",
            self.GpsStatusResponseData,
        )

    class GpsPositionEndpoint:
        def __init__(self, client: PonikaClient) -> None:
            self.client: PonikaClient = client

        class GpsPositionResponseData(BaseModel):
            """Data model for GET /gps/position/status response."""

            accuracy: str
            fix_status: str
            altitude: str
            speed: str
            timestamp: str
            satellites: str
            longitude: str
            latitude: str
            angle: str
            utc_timestamp: str

        def get_status(self) -> ApiResponse[GpsPositionResponseData]:
            """Fetch GPS position status from the device."""
            self.client.logger.info("Accessing GPS position endpoint...")
            return self.client._get(
                "/gps/position/status",
                self.GpsPositionResponseData,
            )


class MessagesEndpoint:
    def __init__(self, client: PonikaClient) -> None:
        self.client: PonikaClient = client

    class MessagesResponseDataItem(BaseModel):
        """Data model for messages response."""

        message: str
        sender: str
        id: str
        modem_id: str
        status: str
        date: str

    # Need to workout how to handle list data responses properly
    # 
    # def get_status(self) -> ApiResponse[List[MessagesResponseDataItem]]:
    #     """Fetch messages from the device."""
    #     self.client.logger.info("Accessing messages endpoint...")
    #     return self.client._get(
    #         "/messages/status",
    #         List[self.MessagesResponseDataItem],
    #     )


def main() -> None:
    pass
