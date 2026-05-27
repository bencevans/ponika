from ponika.endpoints import CRUDEndpoint
from typing import TYPE_CHECKING


from ponika.endpoints.ip_routes.enums import RoutingType
from ponika.models import BaseModel, BasePayload

if TYPE_CHECKING:
    pass


class Ipv4RouteBase:
    interface: str | None = None
    target: str | None = None
    netmask: str | None = None
    gateway: str | None = None
    metric: str | None = None
    mtu: str | None = None
    type: RoutingType | None = None
    table: str | None = None


class Ipv4RouteConfigResponse(BaseModel, Ipv4RouteBase):
    id: str


class Ipv4RouteStatusResponse(BaseModel):
    dev: str
    type: str
    family: str
    table: str
    src: str
    proto: str
    scope: str
    dest: str
    gateway: str


class Ipv4RouteCreatePayload(BasePayload, Ipv4RouteBase): ...


class Ipv4RouteUpdatePayload(BasePayload, Ipv4RouteBase):
    id: str


class IPv4RouteDeleteResponse(BaseModel):
    id: str


class IPv4RouteEndpoint(
    CRUDEndpoint[
        Ipv4RouteCreatePayload,
        Ipv4RouteConfigResponse,
        Ipv4RouteUpdatePayload,
        IPv4RouteDeleteResponse,
    ],
):
    endpoint_path = '/ip_routes/ipv4/config'
    status_endpoint_path = '/ip_routes/ipv4/status'
    allow_status_with_id = False

    config_response_model = Ipv4RouteConfigResponse
    update_model = Ipv4RouteUpdatePayload
    create_model = Ipv4RouteCreatePayload
    delete_reponse_model = IPv4RouteDeleteResponse

    status_response_model = Ipv4RouteStatusResponse
