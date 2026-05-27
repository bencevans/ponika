from examples.config import connection

response = connection.backup.delete()

print(type(response))
print(response)
