from examples.config import connection

connection.firmware.device.download_from_fota()

response = connection.firmware.device.get_progress_status()

print(type(response))
print(response)
