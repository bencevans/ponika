from examples.config import connection

response = connection.wireless.interfaces.get_config()

print(response)
