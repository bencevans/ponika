from examples.config import connection

response = connection.wireguard.peers.config('wg0').delete('peer1')

print(type(response))
print(response)
