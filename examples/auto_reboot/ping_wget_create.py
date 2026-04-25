from examples.config import connection
from ponika.endpoints.auto_reboot.enums import (
    PingWgetAction,
    PingWgetActionWhen,
    PingWgetInterface,
    PingWgetInterval,
    PingWgetIpType,
    PingWgetType,
)
from ponika.endpoints.auto_reboot.ping_wget import PingWgetCreatePayload

payload = PingWgetCreatePayload()
payload.enable = True
payload.stop_action = False
payload.type = PingWgetType.PING
payload.action = PingWgetAction.REBOOT_DEVICE
payload.time = PingWgetInterval.MINUTE_15
payload.interface = PingWgetInterface.WAN
payload.ip_type = PingWgetIpType.IPV4
payload.action_when = PingWgetActionWhen.ALL
payload.host = ['8.8.8.8']

response = connection.auto_reboot.ping_wget.create(payload)

print(type(response))
print(response)
