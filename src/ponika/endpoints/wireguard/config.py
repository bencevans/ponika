from typing import List, Optional

from ponika.endpoints import CRUDEndpoint
from ponika.models import BaseModel, BasePayload


class WireguardConfigBase:
    enabled: Optional[bool] = None
    private_key: Optional[str] = None
    public_key: Optional[str] = None
    listen_port: Optional[str] = None
    addresses: Optional[List[str]] = None
    metric: Optional[str] = None
    mtu: Optional[str] = None
    dns: Optional[List[str]] = None
    watchdog_interval: Optional[str] = None


class WireguardConfigResponse(BaseModel, WireguardConfigBase):
    id: str


class WireguardConfigCreatePayload(BasePayload, WireguardConfigBase):
    id: Optional[str] = None


class WireguardConfigUpdatePayload(BasePayload, WireguardConfigBase):
    id: str


class WireguardConfigDeleteResponse(BaseModel):
    id: str


class ConfigEndpoint(
    CRUDEndpoint[
        WireguardConfigCreatePayload,
        WireguardConfigResponse,
        WireguardConfigUpdatePayload,
        WireguardConfigDeleteResponse,
    ]
):
    endpoint_path = '/wireguard/config'

    config_response_model = WireguardConfigResponse
    create_model = WireguardConfigCreatePayload
    update_model = WireguardConfigUpdatePayload
    delete_reponse_model = WireguardConfigDeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True
