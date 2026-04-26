from typing import List

from pydantic import Field

from ponika.endpoints import CRUDEndpoint
from ponika.endpoints.sms_utilities.enums import (
    DeviceParamType,
    SmsRuleAclMode,
    SmsRuleAction,
    SmsRuleAllowedPhone,
    SmsRuleAuthorization,
    SmsRuleIo,
    SmsRuleMethod,
    SmsRuleSimcard,
)
from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel, BasePayload


class SmsRuleConfigBase:
    enabled: bool | None = None
    action: SmsRuleAction | None = None
    modem_id: str | None = None
    io: SmsRuleIo | None = None
    value: bool | None = None
    timeout: bool | None = None
    seconds: str | None = None
    smstext: str | None = None
    respond: bool | None = None
    status_sms: bool | None = None
    write_config: bool | None = None
    write_wifi: bool | None = None
    write_mobile: bool | None = None
    write_esim: bool | None = None
    to_other_phone: bool | None = None
    to_number: List[str] | None = None
    info_modem_id: str | None = None
    send_modem_id: str | None = None
    message: str | None = None
    simcard: SmsRuleSimcard | None = None
    ssh_access_enabled: bool | None = None
    ssh_access_remote: bool | None = None
    web_access_enabled: bool | None = None
    webs_access_enabled: bool | None = None
    web_access_http: bool | None = None
    web_access_https: bool | None = None
    redirect_https: bool | None = None
    mac: str | None = None
    status_code: bool | None = None
    script: str | None = None
    methods: List[SmsRuleMethod] | None = None
    acl_mode: SmsRuleAclMode | None = None
    authorization: SmsRuleAuthorization | None = None
    allowed_phone: SmsRuleAllowedPhone | None = None
    tel: str | None = None
    group: str | None = None


class SmsRulePayloadBase(SmsRuleConfigBase):
    password: str | None = None


class SmsRuleConfigResponse(BaseModel, SmsRuleConfigBase):
    id: str
    password_set: bool | None = Field(default=None, alias='password:set')


class SmsRuleCreatePayload(BasePayload, SmsRulePayloadBase):
    pass


class SmsRuleUpdatePayload(BasePayload, SmsRulePayloadBase):
    id: str


class SmsRuleDeleteResponse(BaseModel):
    id: str


class DeviceParam(BaseModel):
    type: DeviceParamType
    description: str
    io_name: str | None = None
    block_pins: List[int] | None = None
    id: str


class SmsRuleOptionsResponse(BaseModel):
    actions: List[SmsRuleAction]
    params: List[DeviceParam]


class RulesEndpoint(
    CRUDEndpoint[
        SmsRuleCreatePayload,
        SmsRuleConfigResponse,
        SmsRuleUpdatePayload,
        SmsRuleDeleteResponse,
    ]
):
    endpoint_path = '/sms_utilities/rules/config'

    config_response_model = SmsRuleConfigResponse
    create_model = SmsRuleCreatePayload
    update_model = SmsRuleUpdatePayload
    delete_reponse_model = SmsRuleDeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True

    def get_options(self) -> SmsRuleOptionsResponse:
        response = self._client._get('/sms_utilities/rules/options')
        response_obj = ApiResponse[SmsRuleOptionsResponse].model_validate(
            response
        )

        if not response_obj.success or response_obj.data is None:
            raise TeltonikaApiException(response_obj.errors)

        return response_obj.data
