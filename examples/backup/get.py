from examples.config import connection

response = connection.backup.get_status()

print(type(response))
print(response)
