from examples.config import connection

response = connection.wireguard.peers.config('wg0').delete_bulk(
    ['peer1', 'peer2']
)

print(type(response))
print(response)
