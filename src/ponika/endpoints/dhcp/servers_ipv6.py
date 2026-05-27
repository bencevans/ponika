from ponika.endpoints import (
    CreateEndpoint,
    Endpoint,
    ReadEndpoint,
    StatusEndpoint,
    UpdateEndpoint,
)
from pydantic import ConfigDict, Field
from typing import TYPE_CHECKING, List

from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel, BasePayload

from ponika.endpoints.wireless.enums import WifiMode

if TYPE_CHECKING:
    pass


class DhcpIpv6ServerBase:
    enable_dhcpv6: str | None = None
    ra: WifiMode | None = None
    dhcpv6: WifiMode | None = None
    dynamicdhcp: bool | None = None
    force: bool | None = None
    ndp: str | None = None
    ra_management: str | None = None
    dhcp_option: list[str] | None = None
    ra_default: bool | None = None
    dns: list[str] | None = None
    domain: list[str] | None = None


class DhcpIpv6ServerConfigResponse(BaseModel, DhcpIpv6ServerBase):
    id: str
    interface: str | None = None


class DhcpIpv6ServerCreatePayload(BasePayload, DhcpIpv6ServerBase):
    id: str
    interface: str | None = None


class DhcpIpv6ServerUpdatePayload(BasePayload, DhcpIpv6ServerBase):
    id: str
    # This field is readonly
    interface: str | None = Field(default=None, exclude=True)


class DhcpIpv6ServersStatusResponse(BaseModel):
    class Error(BaseModel):
        error: int
        error_message: float

    id: str
    running: bool
    interface: list[str] | str
    errors: list[Error] | None = None


class DynamicLease(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    class Ipv6Prefix:
        address: str
        prefix_length: int

    expires: int
    duid: str
    ipv6addr: str | list[str] | None = None
    ipv6prefix: Ipv6Prefix | list[Ipv6Prefix] | None = None
    hostname: str
    interface: str


class IPv6ServerEndpoint(
    Endpoint,
    CreateEndpoint[DhcpIpv6ServerCreatePayload, DhcpIpv6ServerConfigResponse],
    ReadEndpoint[DhcpIpv6ServerConfigResponse],
    UpdateEndpoint[DhcpIpv6ServerUpdatePayload, DhcpIpv6ServerConfigResponse],
    StatusEndpoint[DhcpIpv6ServersStatusResponse],
):
    endpoint_path = '/dhcp/servers/ipv4/config'
    status_endpoint_path = '/dhcp/servers/ipv4/status'
    allow_status_with_id = False

    config_response_model = DhcpIpv6ServerConfigResponse
    update_model = DhcpIpv6ServerUpdatePayload
    create_model = DhcpIpv6ServerCreatePayload

    status_response_model = DhcpIpv6ServersStatusResponse

    def get_dynamic_leases(self) -> List[DynamicLease]:
        endpoint = '/dhcp/leases/ipv6/status'

        response = self._client._get(endpoint)

        response = ApiResponse[List[DynamicLease]].model_validate(response)

        if not response.success:
            raise TeltonikaApiException(response.errors)

        if response.data is not None:
            return response.data

        return []
