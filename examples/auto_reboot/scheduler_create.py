from examples.config import connection
from ponika.endpoints.auto_reboot.enums import (
    SchedulerAction,
    SchedulerPeriod,
    SchedulerWeekDay,
)
from ponika.endpoints.auto_reboot.scheduler import SchedulerCreatePayload

payload = SchedulerCreatePayload()
payload.enable = True
payload.action = SchedulerAction.DEVICE_REBOOT
payload.period = SchedulerPeriod.WEEK
payload.days = [SchedulerWeekDay.MONDAY]
payload.time = ['03:00']

response = connection.auto_reboot.scheduler.create(payload)

print(type(response))
print(response)
