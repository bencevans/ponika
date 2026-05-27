from typing import TYPE_CHECKING
from ponika.endpoints.wireless.devices import DevicesEndpoint
from ponika.endpoints.wireless.interfaces import InterfacesEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class WirelessEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client
        self.interfaces = InterfacesEndpoint(client)
        self.devices = DevicesEndpoint(client)
