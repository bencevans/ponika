from examples.config import connection

response = connection.firmware.device.get_progress_status()

print(type(response))
print(response)
