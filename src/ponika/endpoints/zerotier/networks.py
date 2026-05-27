from pydantic import Field

from ponika.endpoints import DynamicPathCRUDEndpoint, Endpoint
from ponika.models import BaseModel, BasePayload


class ZerotierNetworkConfigBase:
    enabled: bool | None = None
    name: str | None = None
    port: str | None = None
    allow_default: bool | None = None
    allow_global: bool | None = None
    allow_managed: bool | None = None
    allow_dns: bool | None = None
    network_id: str | None = None
    bridge_to: str | None = None
    custom_planet_file: str | None = None


class ZerotierNetworkConfigResponse(BaseModel, ZerotierNetworkConfigBase):
    id: str
    custom_planet_file_file_size: int | None = Field(
        default=None,
        alias='custom_planet_file:file_size',
    )


class ZerotierNetworkConfigCreatePayload(
    BasePayload, ZerotierNetworkConfigBase
):
    pass


class ZerotierNetworkConfigUpdatePayload(
    BasePayload, ZerotierNetworkConfigBase
):
    id: str


class ZerotierNetworkConfigDeleteResponse(BaseModel):
    id: str


class NetworkConfigEndpoint(
    DynamicPathCRUDEndpoint[
        ZerotierNetworkConfigCreatePayload,
        ZerotierNetworkConfigResponse,
        ZerotierNetworkConfigUpdatePayload,
        ZerotierNetworkConfigDeleteResponse,
    ]
):
    endpoint_path_template = '/zerotier/{config_id}/networks/config'

    config_response_model = ZerotierNetworkConfigResponse
    create_model = ZerotierNetworkConfigCreatePayload
    update_model = ZerotierNetworkConfigUpdatePayload
    delete_reponse_model = ZerotierNetworkConfigDeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True


class NetworksEndpoint(Endpoint):
    def config(self, config_id: str | int) -> NetworkConfigEndpoint:
        return NetworkConfigEndpoint(self._client, config_id=config_id)
