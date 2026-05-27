from typing import List, Optional

from ponika.endpoints import DynamicPathCRUDEndpoint, Endpoint
from ponika.models import BaseModel, BasePayload


class WireguardPeerEntity:
    public_key: Optional[str] = None
    allowed_ips: Optional[List[str]] = None
    description: Optional[str] = None
    route_allowed_ips: Optional[bool] = None
    preshared_key: Optional[str] = None
    endpoint_host: Optional[str] = None
    endpoint_port: Optional[str] = None
    persistent_keepalive: Optional[str] = None
    table: Optional[str] = None
    tunlink: Optional[str] = None
    force_tunlink: Optional[bool] = None


class WireguardPeerConfigResponse(BaseModel, WireguardPeerEntity):
    id: str


class WireguardPeerDeleteResponse(BaseModel):
    id: str


class WireguardPeerCreateItemPayload(BasePayload, WireguardPeerEntity):
    id: Optional[str] = None


class WireguardPeerUpdateItemPayload(BasePayload, WireguardPeerEntity):
    id: str


class WireguardPeersConfigEndpoint(
    DynamicPathCRUDEndpoint[
        WireguardPeerCreateItemPayload,
        WireguardPeerConfigResponse,
        WireguardPeerUpdateItemPayload,
        WireguardPeerDeleteResponse,
    ]
):
    endpoint_path_template = '/wireguard/{interface_id}/peers/config'

    config_response_model = WireguardPeerConfigResponse
    create_model = WireguardPeerCreateItemPayload
    update_model = WireguardPeerUpdateItemPayload
    delete_reponse_model = WireguardPeerDeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True


class PeersEndpoint(Endpoint):
    def config(self, interface_id: str | int) -> WireguardPeersConfigEndpoint:
        return WireguardPeersConfigEndpoint(
            self._client,
            interface_id=interface_id,
        )
