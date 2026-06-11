from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient


class SimCardsEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self._client: "PonikaClient" = client

    class GetSimCardConfig(BaseModel):
        band: str
        deny_roaming: Literal["0", "1"]
        enable_sms_limit: Literal["0", "1"]
        id: str
        modem: str
        nr5g_mode: str
        operator: str
        operlist: Literal["0", "1"]
        position: str
        primary: Literal["0", "1"]
        service: str
        signal_reset_enabled: Literal["0", "1"]
        signal_reset_threshold: Optional[str] = None
        signal_reset_timeout: Optional[str] = None
        volte: str

    def get_config(
        self,
    ) -> "ApiResponse[List[GetSimCardConfig]]":
        """Fetch global SIM card config."""
        return ApiResponse[List[self.GetSimCardConfig]].model_validate(
            self._client._get("/sim_cards/config")
        )
