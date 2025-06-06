from typing import Optional
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient


class DhcpEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self.client: "PonikaClient" = client
        self.leases = self.DhcpLeasesEndpoint(client)

    class DhcpLeasesEndpoint:
        def __init__(self, client: "PonikaClient") -> None:
            self.client: "PonikaClient" = client
            self.ipv4 = self.DhcpLeasesIpv4Endpoint(client)

        class DhcpLeasesIpv4Endpoint:
            def __init__(self, client: "PonikaClient") -> None:
                self.client: "PonikaClient" = client

            class DhcpLeasesIpv4ResponseDataItem(BaseModel):
                """Data model for IPv4 DHCP leases response."""

                expires: Optional[int] = Field(
                    description="Amount of time left for DHCP lease to expire."
                )
                macaddr: Optional[str] = Field(description="MAC address of the device.")
                ipaddr: Optional[str] = Field(
                    description="IP address assigned to the device."
                )
                hostname: Optional[str] = Field(
                    default=None, description="Hostname of the device, if available."
                )
                interface: Optional[str] = Field(
                    default=None,
                    description="Network interface the device is connected to.",
                )

            def get_status(
                self,
            ) -> "ApiResponse[list[DhcpLeasesIpv4ResponseDataItem]]":
                """Fetch IPv4 DHCP leases from the device."""
                return ApiResponse[
                    list[self.DhcpLeasesIpv4ResponseDataItem]
                ].model_validate(self.client._get("/dhcp/leases/ipv4/status"))
