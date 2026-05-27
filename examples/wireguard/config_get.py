from examples.config import connection

response = connection.wireguard.config.get_config('wg0')

print(type(response))
print(response)
