from ponika.endpoints import (
    CreateEndpoint,
    Endpoint,
    ReadEndpoint,
    StatusEndpoint,
    UpdateEndpoint,
)
from pydantic import Field
from typing import TYPE_CHECKING, List

from ponika.endpoints.dhcp.enums import DHCPMode
from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel, BasePayload


if TYPE_CHECKING:
    pass


class DhcpIpv4ServerBase:
    enable_dhcpv4: str | None = None
    mode: DHCPMode | None = None
    server_relay: str | None = None
    circuit_id: str | None = None
    remote_id: str | None = None
    start_ip: str | None = None
    end_ip: str | None = None
    leasetime: str | None = None
    dynamicdhcp: bool | None = None
    force: bool | None = None
    netmask: str | None = None
    dhcp_option: list[str] | None = None
    force_options: bool | None = None


class DhcpIpv4ServerConfigResponse(BaseModel, DhcpIpv4ServerBase):
    id: str
    interface: str | None = None


class DhcpIpv4ServerCreatePayload(BasePayload, DhcpIpv4ServerBase):
    id: str
    interface: str | None = None


class DhcpIpv4ServerUpdatePayload(BasePayload, DhcpIpv4ServerBase):
    id: str
    # This field is readonly
    interface: str | None = Field(default=None, exclude=True)


class DhcpIpv4ServersStatusResponse(BaseModel):
    class Error(BaseModel):
        error: int
        error_message: float

    id: str
    running: bool
    interface: list[str] | str
    errors: list[Error] | None = None


class DynamicLease(BaseModel):
    expires: int
    macaddr: str
    ipaddr: str
    hostname: str
    interface: str


class IPv4ServerEndpoint(
    Endpoint,
    CreateEndpoint[DhcpIpv4ServerCreatePayload, DhcpIpv4ServerConfigResponse],
    ReadEndpoint[DhcpIpv4ServerConfigResponse],
    UpdateEndpoint[DhcpIpv4ServerUpdatePayload, DhcpIpv4ServerConfigResponse],
    StatusEndpoint[DhcpIpv4ServersStatusResponse],
):
    endpoint_path = '/dhcp/servers/ipv4/config'
    status_endpoint_path = '/dhcp/servers/ipv4/status'
    allow_status_with_id = False

    config_response_model = DhcpIpv4ServerConfigResponse
    update_model = DhcpIpv4ServerUpdatePayload
    create_model = DhcpIpv4ServerCreatePayload

    status_response_model = DhcpIpv4ServersStatusResponse

    def get_dynamic_leases(self) -> List[DynamicLease]:
        endpoint = '/dhcp/leases/ipv4/status'

        response = self._client._get(endpoint)

        response = ApiResponse[List[DynamicLease]].model_validate(response)

        if not response.success:
            raise TeltonikaApiException(response.errors)

        if response.data is not None:
            return response.data

        return []
