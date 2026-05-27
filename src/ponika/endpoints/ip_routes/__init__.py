from typing import TYPE_CHECKING

from ponika.endpoints.ip_routes.ipv4 import IPv4RouteEndpoint
from ponika.endpoints.ip_routes.ipv6 import Ipv6RouteEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class IPRouteEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client
        self.routes_ipv4 = IPv4RouteEndpoint(client)
        self.routes_ipv6 = Ipv6RouteEndpoint(client)
