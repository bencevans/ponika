from examples.config import connection

response = connection.wireguard.peers.config('wg0').get_config()

print(type(response))
print(response)
