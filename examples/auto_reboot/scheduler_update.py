from examples.config import connection
from ponika.endpoints.auto_reboot.enums import SchedulerWeekDay

target_endpoint = connection.auto_reboot.scheduler
response = target_endpoint.get_config()[0]

update_payload = connection.auto_reboot.scheduler.config_to_update_payload(
    response
)
update_payload.enable = False
update_payload.days = [SchedulerWeekDay.WEDNESDAY, SchedulerWeekDay.THURSDAY]
update_payload.time = ['04:00']

response = connection.auto_reboot.scheduler.update(update_payload)

print(type(response))
print(response)
