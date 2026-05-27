from ponika.endpoints import CRUDEndpoint
from ponika.models import BaseModel, BasePayload


class ZerotierConfigBase:
    enabled: bool | None = None
    name: str | None = None


class ZerotierConfigResponse(BaseModel, ZerotierConfigBase):
    id: str
    node_id: str | None = None


class ZerotierConfigCreatePayload(BasePayload, ZerotierConfigBase):
    pass


class ZerotierConfigUpdatePayload(BasePayload, ZerotierConfigBase):
    id: str


class ZerotierConfigDeleteResponse(BaseModel):
    id: str


class ConfigEndpoint(
    CRUDEndpoint[
        ZerotierConfigCreatePayload,
        ZerotierConfigResponse,
        ZerotierConfigUpdatePayload,
        ZerotierConfigDeleteResponse,
    ]
):
    endpoint_path = '/zerotier/config'

    config_response_model = ZerotierConfigResponse
    create_model = ZerotierConfigCreatePayload
    update_model = ZerotierConfigUpdatePayload
    delete_reponse_model = ZerotierConfigDeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True
