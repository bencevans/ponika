from typing import Dict, List, Literal
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient


class ModemsEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self._client: "PonikaClient" = client

    class GetModemsStatusOffline(BaseModel):
        """Data model for GET /modems/status response when modem is offline."""

        id: str
        """Offline modem id."""

        name: str
        """Offline modem name."""

        offline: Literal[0, 1]

        blocked: Literal[0, 1]

        builtin: bool

        primary: bool

        sim_count: int

        mode: int

        multi_apn: bool
        operators_scan: bool
        dynamic_mtu: bool
        ipv6: bool
        volte: bool

    class GetModemsStatusOnline(BaseModel):
        """Data model for GET /modems/status response."""

        id: str
        imei: str
        model: str

        class CellInfo(BaseModel):
            """Data model for cell information in modem status."""

            mcc: str
            mnc: str
            cellid: str
            ue_state: int
            lac: str
            tac: str
            pcid: int
            earfcn: int
            arfcn: str
            uarfcn: str
            nr_arfcn: str = Field(alias="nr-arfcn")
            rsrp: str
            rsrq: str
            sinr: int
            bandwidth: str

        cell_info: List[CellInfo]
        dynamic_mtu: bool
        service_modes: Dict[str, List[str]]
        lac: str
        tac: str
        name: str
        # index: str
        sim_count: int
        version: str
        manufacturer: str
        builtin: bool
        mode: int
        primary: int
        multi_apn: bool
        ipv6: bool
        volte_supported: bool
        auto_3g_bands: bool
        operators_scan: bool
        mobile_dfota: bool
        no_ussd: bool
        framed_routing: bool
        low_signal_reconnect: bool
        active_sim: int
        conntype: str
        simstate: str
        simstate_id: int
        data_conn_state: str
        data_conn_state_id: int
        txbytes: int
        rxbytes: int
        baudrate: int
        is_busy: int
        data_off: bool
        busy_state: str
        busy_state_id: int
        pinstate: str
        pinstate_id: int
        operator_state: str
        operator_state_id: int
        rssi: int
        operator: str
        provider: str
        ntype: str
        imsi: str
        iccid: str
        cellid: str
        # rscp: str
        # ecio: str
        rsrp: int
        rsrq: int
        sinr: int
        pinleft: int
        volte: bool
        sc_band_av: str

        class CarrierAggregationSignal(BaseModel):
            """Data model for carrier aggregation signal in modem status."""

            band: str
            bandwidth: str
            sinr: int
            rsrq: int
            rsrp: int
            pcid: int
            frequency: int

        ca_signal: List[CarrierAggregationSignal] = Field(default_factory=list)

        temperature: int
        """Optional field for modem temperature."""

        mobile_stage: int

    def get_status(
        self,
    ) -> "ApiResponse[List[GetModemsStatusOnline | GetModemsStatusOffline]]":
        """Fetch global GPS config."""
        return ApiResponse[
            List[self.GetModemsStatusOnline | self.GetModemsStatusOffline]
        ].model_validate(self._client._get("/modems/status"))
