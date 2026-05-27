from examples.config import connection

response = connection.wireguard.config.delete('wg0')

print(type(response))
print(response)
