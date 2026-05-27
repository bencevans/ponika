from examples.config import connection

response = connection.wireless.interfaces.delete(1)

print(type(response))
print(response)
