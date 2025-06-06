from typing import List, Literal, Optional
from pydantic import BaseModel
from typing import TYPE_CHECKING

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient


class TailscaleEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self.client: "PonikaClient" = client

    class TailscaleConfigResponseDataItem(BaseModel):
        """Data model for Tailscale configuration response."""

        id: Optional[str] = None
        enabled: Optional[str] = None
        auth_key: Optional[str] = None
        advert_routes: Optional[List[str]] = None
        accept_routes: Optional[str] = None
        exit_node: Optional[str] = None
        auth_type: Literal["url", "key"]
        default_route: Optional[Literal["0", "1"]] = None
        exit_node_ip: Optional[str] = None
        login_server: Optional[str] = None

    def get_config(self) -> "ApiResponse[List[TailscaleConfigResponseDataItem]]":
        """Fetch Tailscale configuration from the device."""
        return ApiResponse[List[self.TailscaleConfigResponseDataItem]].model_validate(
            self.client._get("/tailscale/config")
        )

    class TailscaleStatusResponseDataItem(BaseModel):
        """Data model for Tailscale status response."""

        status: str
        url: str
        ip: List[str]
        message: List[str]

    def get_status(self) -> "ApiResponse[List[TailscaleStatusResponseDataItem]]":
        """Fetch Tailscale status from the device."""
        return ApiResponse[List[self.TailscaleStatusResponseDataItem]].model_validate(
            self.client._get("/tailscale/status")
        )
