from typing import List, Literal, Optional

from ponika.endpoints import (
    Endpoint,
    ReadEndpoint,
    StatusEndpoint,
    UpdateEndpoint,
)
from ponika.models import BaseModel, BasePayload


class TailscaleConfigBase:
    enabled: Optional[str] = None
    auth_key: Optional[str] = None
    advert_routes: Optional[List[str]] = None
    accept_routes: Optional[str] = None
    exit_node: Optional[str] = None
    auth_type: Literal['url', 'key']
    default_route: Optional[Literal['0', '1']] = None
    exit_node_ip: Optional[str] = None
    login_server: Optional[str] = None


class TailscaleConfigResponse(BaseModel, TailscaleConfigBase):
    id: Optional[str] = None


class TailscaleConfigUpdatePayload(BasePayload, TailscaleConfigBase):
    """Payload for both single-item and bulk Tailscale updates."""


class TailscaleStatusResponse(BaseModel):
    status: str
    url: str
    ip: List[str]
    message: List[str]


class TailscaleEndpoint(
    Endpoint,
    ReadEndpoint[TailscaleConfigResponse],
    UpdateEndpoint[TailscaleConfigUpdatePayload, TailscaleConfigResponse],
    StatusEndpoint[TailscaleStatusResponse],
):
    endpoint_path = '/tailscale/config'
    status_endpoint_path = '/tailscale/status'
    allow_status_with_id = False
    allow_bulk_update = True

    config_response_model = TailscaleConfigResponse
    update_model = TailscaleConfigUpdatePayload
    status_response_model = TailscaleStatusResponse
