from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ponika import PonikaClient, ApiResponse


class UnauthorizedEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self.client: "PonikaClient" = client

    class UnauthorizedStatusResponseData(BaseModel):
        """Data model for GET /unauthorized/status response."""

        device_name: str
        device_model: str
        device_identifier: str
        api_version: str
        lang: str

    def get_status(self) -> "ApiResponse[UnauthorizedStatusResponseData]":
        """Fetch unauthorized status from the device."""
        self.client.logger.info("Accessing unauthorized endpoint...")
        return ApiResponse[self.UnauthorizedStatusResponseData].model_validate(
            self.client._get(
                "/unauthorized/status",
            )
        )
