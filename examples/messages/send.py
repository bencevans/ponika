from examples.config import connection

response = connection.messages.send(
    number='+49123456789',
    message='Hello from ponika',
    modem='1-1',
)

print(type(response))
print(response)
