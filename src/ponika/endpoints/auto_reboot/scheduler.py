from typing import List

from ponika.endpoints import CRUDEndpoint
from ponika.endpoints.auto_reboot.enums import (
    SchedulerAction,
    SchedulerMonth,
    SchedulerMonthDay,
    SchedulerPeriod,
    SchedulerWeekDay,
)
from ponika.models import BaseModel, BasePayload


class SchedulerConfigBase:
    enable: bool | None = None
    action: SchedulerAction | None = None
    modem: str | None = None
    period: SchedulerPeriod | None = None
    days: List[SchedulerWeekDay] | None = None
    time: List[str] | None = None
    month_day: List[SchedulerMonthDay] | None = None
    months: List[SchedulerMonth] | None = None
    force_last: bool | None = None


class SchedulerConfigResponse(BaseModel, SchedulerConfigBase):
    id: str


class SchedulerCreatePayload(BasePayload, SchedulerConfigBase):
    pass


class SchedulerUpdatePayload(BasePayload, SchedulerConfigBase):
    id: str


class SchedulerDeleteResponse(BaseModel):
    id: str


class SchedulerEndpoint(
    CRUDEndpoint[
        SchedulerCreatePayload,
        SchedulerConfigResponse,
        SchedulerUpdatePayload,
        SchedulerDeleteResponse,
    ]
):
    endpoint_path = '/auto_reboot/scheduler/config'

    config_response_model = SchedulerConfigResponse
    create_model = SchedulerCreatePayload
    update_model = SchedulerUpdatePayload
    delete_reponse_model = SchedulerDeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True
