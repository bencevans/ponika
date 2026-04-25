from typing import List

from ponika.endpoints import CRUDEndpoint
from ponika.endpoints.auto_reboot.enums import (
    PingWgetAction,
    PingWgetActionWhen,
    PingWgetInterface,
    PingWgetInterval,
    PingWgetIpType,
    PingWgetType,
)

from ponika.models import BaseModel, BasePayload


class PingWgetConfigBase:
    enable: bool | None = None
    stop_action: bool | None = None
    type: PingWgetType | None = None
    action: PingWgetAction | None = None
    modem_id_sms: str | None = None
    number: List[str] | None = None
    message: str | None = None
    modem: str | None = None
    time: PingWgetInterval | None = None
    retry: str | None = None
    time_out: str | None = None
    packet_size: str | None = None
    interface: PingWgetInterface | None = None
    ip_type: PingWgetIpType | None = None
    url: List[str] | None = None
    action_when: PingWgetActionWhen | None = None
    host: List[str] | None = None
    ip_type1: PingWgetIpType | None = None
    host1: List[str] | None = None


class PingWgetConfigResponse(BaseModel, PingWgetConfigBase):
    id: str


class PingWgetCreatePayload(BasePayload, PingWgetConfigBase):
    pass


class PingWgetUpdatePayload(BasePayload, PingWgetConfigBase):
    id: str


class PingWgetDeleteResponse(BaseModel):
    id: str


class PingWgetEndpoint(
    CRUDEndpoint[
        PingWgetCreatePayload,
        PingWgetConfigResponse,
        PingWgetUpdatePayload,
        PingWgetDeleteResponse,
    ]
):
    endpoint_path = '/auto_reboot/ping_wget/config'

    config_response_model = PingWgetConfigResponse
    create_model = PingWgetCreatePayload
    update_model = PingWgetUpdatePayload
    delete_reponse_model = PingWgetDeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True
