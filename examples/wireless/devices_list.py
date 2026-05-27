from examples.config import connection

response = connection.wireless.devices.get_config()

print(response)
