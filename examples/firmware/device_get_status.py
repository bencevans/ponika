from examples.config import connection

response = connection.firmware.device.get_status()

print(type(response))
print(response)
