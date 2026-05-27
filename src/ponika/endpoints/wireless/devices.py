from ponika.endpoints import (
    Endpoint,
    ReadEndpoint,
    StatusEndpoint,
    UpdateEndpoint,
)
from typing import TYPE_CHECKING, Optional

from ponika.models import BaseModel, BasePayload

from ponika.endpoints.wireless.enums import WifiDeviceBand

if TYPE_CHECKING:
    pass


class WirelessDeviceBase:
    enabled: bool | str = True
    hwmode: Optional[str] = None
    channel: Optional[str] = None
    htmode: Optional[str] = None
    txpower: Optional[str] = None
    tx_power: Optional[str] = None
    country: Optional[str] = None
    legacy_rates: Optional[str] = None
    distance: Optional[str] = None
    frag: Optional[str] = None
    rts: Optional[str] = None
    noscan: Optional[str] = None
    beacon_int: Optional[str] = None
    acs_exclude_dfs: Optional[str] = None


class WirelessDeviceConfigResponse(BaseModel, WirelessDeviceBase):
    id: Optional[str] = None


class WirelessDeviceUpdatePayload(BasePayload, WirelessDeviceBase):
    id: str


class WirelessDevicesStatusResponse(BaseModel):
    """Data model for wireless interfaces response."""

    class HardwareId(BaseModel):
        device_id: float
        subsystem_device_id: float
        vendor_id: float
        subsystem_vendor_id: float

    id: str
    quality_max: float
    disabled: bool
    hardware_name: str
    phyname: str
    mode: str
    txpower_offset: float
    type: str
    hardware_id: HardwareId
    country: str
    standard: str
    pending: bool
    # txpower: float
    name: str
    # channel: float
    autostart: bool
    up: bool
    noise: float
    # frequency: float
    band: WifiDeviceBand | None = None
    macaddr: str | None = None


class DevicesEndpoint(
    Endpoint,
    ReadEndpoint[WirelessDeviceConfigResponse],
    UpdateEndpoint[WirelessDeviceUpdatePayload, WirelessDeviceConfigResponse],
    StatusEndpoint[WirelessDevicesStatusResponse],
):
    endpoint_path = '/wireless/devices/config'
    status_endpoint_path = '/wireless/devices/status'

    config_response_model = WirelessDeviceConfigResponse
    update_model = WirelessDeviceUpdatePayload

    status_response_model = WirelessDevicesStatusResponse
