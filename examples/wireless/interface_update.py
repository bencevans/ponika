from examples.config import connection

response = connection.wireless.interfaces.get_config(1)

update_payload = connection.wireless.interfaces.config_to_update_payload(
    response
)
update_payload.enabled = False

response = connection.wireless.interfaces.update(update_payload)

print(type(response))
print(response)
