from examples.config import connection

response = connection.backup.download()

print(type(response))
print(response)
