from pydantic import BaseModel
from typing import TYPE_CHECKING, List, Optional

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient


class WirelessEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self.client: "PonikaClient" = client
        self.interfaces = self.InterfacesEndpoint(client)

    class InterfacesEndpoint:
        def __init__(self, client: "PonikaClient") -> None:
            self.client: "PonikaClient" = client

        class InterfacesResponseDataItem(BaseModel):
            """Data model for wireless interfaces response."""

            class Client(BaseModel):
                """Data model for wireless client information."""
                expires: int
                band: str
                ipaddr: str
                hostname: Optional[str] = None
                tx_rate: int
                macaddr: str
                rx_rate: int
                signal: str
                interface: str
                device: str

            wifi_id: str
            ifname: str
            disabled: bool
            encryption: str
            vht_supported: Optional[bool] = None # differs from docs says is required
            bssid: str
            num_assoc: int
            clients: List[Client] = []
            status: str
            mode: Optional[str] = None
            multiple: Optional[bool] = None
            # ht_supported: bool
            ssid: str
            id: str
            # conf_id: str
            # auth_status: int



        def get_status(self) -> "ApiResponse[list[InterfacesResponseDataItem]]":
            """Fetch wireless interfaces status from the device."""
            return ApiResponse[list[self.InterfacesResponseDataItem]].model_validate(
                self.client._get("/wireless/interfaces/status")
            )
