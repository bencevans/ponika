from examples.config import connection

response = connection.wireless.interfaces.get_config(1)

print(response)
