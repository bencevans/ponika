from typing import TYPE_CHECKING

from ponika.endpoints.wireguard.actions import ActionsEndpoint
from ponika.endpoints.wireguard.config import ConfigEndpoint
from ponika.endpoints.wireguard.peers import PeersEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class WireguardEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client
        self.config = ConfigEndpoint(client)
        self.actions = ActionsEndpoint(client)
        self.peers = PeersEndpoint(client)
