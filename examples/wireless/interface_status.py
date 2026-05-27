from examples.config import connection

response = connection.wireless.interfaces.get_status()

print(type(response))
print(response)
print(response[0].ssid)

response = connection.wireless.interfaces.get_status(1)

print(type(response))
print(response)
