from examples.config import connection

response = connection.wireless.devices.get_config('radio0')

print(response)
