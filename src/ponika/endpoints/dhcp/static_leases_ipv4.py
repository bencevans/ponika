from ponika.endpoints import CRUDEndpoint
from ponika.models import BaseModel, BasePayload


class StaticLeaseIpv4Base:
    name: str | None = None
    mac: str | None = None
    ip: str | None = None


class StaticLeaseIpv4ConfigResponse(BaseModel, StaticLeaseIpv4Base):
    id: str


class StaticLeaseIpv4CreatePayload(BasePayload, StaticLeaseIpv4Base):
    pass


class StaticLeaseIpv4UpdatePayload(BasePayload, StaticLeaseIpv4Base):
    id: str


class StaticLeaseIpv4DeleteResponse(BaseModel):
    id: str


class StaticLeasesIPv4Endpoint(
    CRUDEndpoint[
        StaticLeaseIpv4CreatePayload,
        StaticLeaseIpv4ConfigResponse,
        StaticLeaseIpv4UpdatePayload,
        StaticLeaseIpv4DeleteResponse,
    ]
):
    endpoint_path = '/dhcp/static_leases/ipv4/config'

    config_response_model = StaticLeaseIpv4ConfigResponse
    create_model = StaticLeaseIpv4CreatePayload
    update_model = StaticLeaseIpv4UpdatePayload
    delete_reponse_model = StaticLeaseIpv4DeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True
