from examples.config import connection
from ponika.config import AutoRebootConfig, PonikaConfig
from ponika.endpoints.auto_reboot.enums import (
    PingWgetAction,
    PingWgetActionWhen,
    PingWgetInterface,
    PingWgetInterval,
    PingWgetIpType,
    PingWgetType,
    SchedulerAction,
    SchedulerPeriod,
    SchedulerWeekDay,
)
from ponika.endpoints.auto_reboot.ping_wget import PingWgetCreatePayload
from ponika.endpoints.auto_reboot.scheduler import SchedulerCreatePayload

scheduler = SchedulerCreatePayload()
scheduler.enable = True
scheduler.action = SchedulerAction.DEVICE_REBOOT
scheduler.period = SchedulerPeriod.WEEK
scheduler.days = [SchedulerWeekDay.MONDAY]
scheduler.time = ['03:00']

ping_wget = PingWgetCreatePayload()
ping_wget.enable = True
ping_wget.stop_action = False
ping_wget.type = PingWgetType.PING
ping_wget.action = PingWgetAction.REBOOT_DEVICE
ping_wget.time = PingWgetInterval.MINUTE_15
ping_wget.interface = PingWgetInterface.WAN
ping_wget.ip_type = PingWgetIpType.IPV4
ping_wget.action_when = PingWgetActionWhen.ALL
ping_wget.host = ['8.8.8.8']

desired_config = PonikaConfig(
    auto_reboot=AutoRebootConfig(
        scheduler=[scheduler],
        ping_wget=[ping_wget],
    )
)

preview = connection.config.apply(
    desired_config,
    dry_run=True,
    delete_unmanaged=False,
)
print(preview.changes)

result = connection.config.apply(
    desired_config,
    delete_unmanaged=False,
)
print(result)
