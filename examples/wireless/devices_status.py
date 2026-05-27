from examples.config import connection

response = connection.wireless.devices.get_status()

print(type(response))
print(response)

response = connection.wireless.devices.get_status('radio0')

print(type(response))
print(response)
