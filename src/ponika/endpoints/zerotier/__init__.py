from typing import TYPE_CHECKING

from ponika.endpoints.zerotier.config import ConfigEndpoint
from ponika.endpoints.zerotier.networks import NetworksEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class ZerotierEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client
        self.config = ConfigEndpoint(client)
        self.networks = NetworksEndpoint(client)
