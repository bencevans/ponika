from pydantic import BaseModel, Field
from typing import TYPE_CHECKING

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient


class InternetConnectionEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self.client: "PonikaClient" = client

    class InternetStatusResponseData(BaseModel):
        """Data model for Internet status response."""

        ipv4_status: str = Field(
            description="Indicates whether the device is connected to the internet."
        )
        ipv6_status: str = Field(
            description="IPv6 address of the device, if available."
        )
        dns_status: str = Field(description="DNS status of the device, if available.")

    def get_status(self) -> "ApiResponse[InternetStatusResponseData]":
        """Fetch Internet status from the device."""
        return ApiResponse[self.InternetStatusResponseData].model_validate(
            self.client._get("/internet_connection/status")
        )
