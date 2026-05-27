from typing import TYPE_CHECKING

from ponika.endpoints.sms_utilities.rules import RulesEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class SmsUtilitiesEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client
        self.rules = RulesEndpoint(client)
