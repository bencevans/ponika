from examples.config import connection


response = connection.wireless.devices.get_config('radio0')

update_payload = connection.wireless.devices.config_to_update_payload(response)
update_payload.enabled = True

response = connection.wireless.devices.update(update_payload)

print(type(response))
print(response)
