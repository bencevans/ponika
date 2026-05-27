from typing import TYPE_CHECKING

from ponika.endpoints.auto_reboot.ping_wget import PingWgetEndpoint
from ponika.endpoints.auto_reboot.scheduler import SchedulerEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class AutoRebootEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client
        self.scheduler = SchedulerEndpoint(client)
        self.ping_wget = PingWgetEndpoint(client)
