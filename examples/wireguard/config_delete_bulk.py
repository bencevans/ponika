from examples.config import connection

response = connection.wireguard.config.delete_bulk(['wg0', 'wg1'])

print(type(response))
print(response)
