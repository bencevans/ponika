from examples.config import connection

response = connection.messages.read()

print(type(response))
print(response)
