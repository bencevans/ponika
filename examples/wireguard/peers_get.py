from examples.config import connection

response = connection.wireguard.peers.config('wg0').get_config('peer1')

print(type(response))
print(response)
