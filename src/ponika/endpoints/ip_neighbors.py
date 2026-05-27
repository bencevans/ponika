from typing import List, Optional
from pydantic import BaseModel
from typing import TYPE_CHECKING

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient


class IpNeighborsEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client
        self.ipv4 = self.Ipv4NeighborsEndpoint(client)
        self.ipv6 = self.Ipv6NeighborsEndpoint(client)

    class Ipv4NeighborsEndpoint:
        def __init__(self, client: 'PonikaClient') -> None:
            self._client: 'PonikaClient' = client

        class Ipv4NeighborResponseDataItem(BaseModel):
            """Data model for IPv4 neighbor response."""

            proxy: str
            stale: str
            noarp: str
            incomplete: str
            delay: str
            family: str
            reachable: str
            mac: Optional[str] = None
            dev: str
            router: str
            dest: str
            probe: str
            failed: str
            permanent: str

        def get_status(
            self,
        ) -> 'ApiResponse[List[Ipv4NeighborResponseDataItem]]':
            """Fetch IPv4 neighbors from the device."""
            return ApiResponse[
                List[self.Ipv4NeighborResponseDataItem]
            ].model_validate(self._client._get('/ip_neighbors/ipv4/status'))

    class Ipv6NeighborsEndpoint:
        def __init__(self, client: 'PonikaClient') -> None:
            self._client: 'PonikaClient' = client

        class Ipv6NeighborResponseDataItem(BaseModel):
            """Data model for IPv6 neighbor response."""

            proxy: str
            stale: str
            noarp: str
            incomplete: str
            delay: str
            family: str
            reachable: str
            mac: Optional[str] = None
            dev: str
            router: str
            dest: str
            probe: str
            failed: str
            permanent: str

        def get_status(
            self,
        ) -> 'ApiResponse[List[Ipv6NeighborResponseDataItem]]':
            """Fetch IPv6 neighbors from the device."""
            return ApiResponse[
                List[self.Ipv6NeighborResponseDataItem]
            ].model_validate(self._client._get('/ip_neighbors/ipv6/status'))
