from pydantic import BaseModel
from typing import TYPE_CHECKING

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient


class SessionEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self.client: "PonikaClient" = client

    class SessionResponseData(BaseModel):
        """Data model for session response."""

        active: bool

    def get_status(self) -> "ApiResponse[SessionResponseData]":
        """Fetch session information from the device."""

        return ApiResponse[self.SessionResponseData].model_validate(
            self.client._get("/session/status")
        )
