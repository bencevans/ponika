from ponika.endpoints import CRUDEndpoint

from ponika.endpoints.ip_routes.enums import RoutingType
from ponika.models import BaseModel, BasePayload


class Ipv6RouteBase:
    interface: str | None = None
    target: str | None = None
    gateway: str | None = None
    metric: str | None = None
    mtu: str | None = None
    type: RoutingType | None = None
    table: str | None = None


class Ipv6RouteConfigResponse(BaseModel, Ipv6RouteBase):
    id: str


class Ipv6RouteStatusResponse(BaseModel):
    dev: str
    type: str
    family: str
    table: str
    metric: str
    proto: str
    scope: str
    dest: str
    gateway: str


class Ipv6RouteUpdatePayload(BasePayload, Ipv6RouteBase):
    id: str


class Ipv6RouteDeleteResponse(BaseModel):
    id: str


class Ipv6RouteCreatePayload(BasePayload, Ipv6RouteBase):
    pass


class Ipv6RouteEndpoint(
    CRUDEndpoint[
        Ipv6RouteCreatePayload,
        Ipv6RouteConfigResponse,
        Ipv6RouteUpdatePayload,
        Ipv6RouteDeleteResponse,
    ],
):
    endpoint_path = '/ip_routes/ipv6/config'
    status_endpoint_path = '/ip_routes/ipv6/status'
    allow_status_with_id = False

    config_response_model = Ipv6RouteConfigResponse
    update_model = Ipv6RouteUpdatePayload
    create_model = Ipv6RouteCreatePayload
    delete_reponse_model = Ipv6RouteDeleteResponse

    status_response_model = Ipv6RouteStatusResponse
