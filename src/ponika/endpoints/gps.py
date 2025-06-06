from typing import Literal, Optional
from pydantic import BaseModel
from typing import TYPE_CHECKING

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient


class GpsEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self.client: "PonikaClient" = client
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

    def get_global(self) -> "ApiResponse[GetGlobalResponseData]":
        """Fetch global GPS config."""
        return ApiResponse[self.GetGlobalResponseData].model_validate(
            self.client._get("/gps/global")
        )

    class GpsStatusResponseData(BaseModel):
        """Data model for GET /gps/status response."""

        dpo_support: bool
        uptime: int

    def get_status(self) -> "ApiResponse[GpsStatusResponseData]":
        """Fetch GPS status from the device."""
        return ApiResponse[self.GpsStatusResponseData].model_validate(
            self.client._get("/gps/status")
        )

    class GpsPositionEndpoint:
        def __init__(self, client: "PonikaClient") -> None:
            self.client: "PonikaClient" = client

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

        def get_status(self) -> "ApiResponse[GpsPositionResponseData]":
            """Fetch GPS position status from the device."""

            return ApiResponse[self.GpsPositionResponseData].model_validate(
                self.client._get("/gps/position/status")
            )
