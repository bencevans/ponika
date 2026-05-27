from ponika.endpoints import CRUDEndpoint
from ponika.models import BaseModel, BasePayload


class StaticLeaseIpv6Base:
    name: str | None = None
    duid: str | None = None
    hostid: str | None = None


class StaticLeaseIpv6ConfigResponse(BaseModel, StaticLeaseIpv6Base):
    id: str


class StaticLeaseIpv6CreatePayload(BasePayload, StaticLeaseIpv6Base):
    pass


class StaticLeaseIpv6UpdatePayload(BasePayload, StaticLeaseIpv6Base):
    id: str


class StaticLeaseIpv6DeleteResponse(BaseModel):
    id: str


class StaticLeasesIPv6Endpoint(
    CRUDEndpoint[
        StaticLeaseIpv6CreatePayload,
        StaticLeaseIpv6ConfigResponse,
        StaticLeaseIpv6UpdatePayload,
        StaticLeaseIpv6DeleteResponse,
    ]
):
    endpoint_path = '/dhcp/static_leases/ipv6/config'

    config_response_model = StaticLeaseIpv6ConfigResponse
    create_model = StaticLeaseIpv6CreatePayload
    update_model = StaticLeaseIpv6UpdatePayload
    delete_reponse_model = StaticLeaseIpv6DeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True
