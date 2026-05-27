from examples.config import connection

response = connection.zerotier.config.delete('1')

print(type(response))
print(response)
