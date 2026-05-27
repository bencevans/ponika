from examples.config import connection

response = connection.firmware.device.get_fota_update_status()

print(type(response))
print(response)
