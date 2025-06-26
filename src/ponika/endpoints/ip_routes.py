from typing import List, Optional
from pydantic import BaseModel
from typing import TYPE_CHECKING

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient


class IpRoutesEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self.client: "PonikaClient" = client
        self.ipv4 = self.Ipv4RoutesEndpoint(client)

    class Ipv4RoutesEndpoint:
        def __init__(self, client: "PonikaClient") -> None:
            self.client: "PonikaClient" = client

        class Ipv4RouteResponseDataItem(BaseModel):
            """Data model for IPv4 route response."""

            dev: str
            type: str
            family: str
            table: str
            src: Optional[str] = None
            proto: str
            scope: str
            dest: str
            gateway: Optional[str] = None

        def get_status(self) -> "ApiResponse[List[Ipv4RouteResponseDataItem]]":
            """Fetch IPv4 routes from the device."""
            return ApiResponse[List[self.Ipv4RouteResponseDataItem]].model_validate(
                self.client._get("/ip_routes/ipv4/status")
            )
