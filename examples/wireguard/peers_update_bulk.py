from examples.config import connection
from ponika.endpoints.wireguard.peers import WireguardPeerUpdateItemPayload

payload1 = WireguardPeerUpdateItemPayload(id='peer1')
payload1.public_key = 'p' * 44
payload1.allowed_ips = ['10.10.0.2/32']

payload2 = WireguardPeerUpdateItemPayload(id='peer2')
payload2.public_key = 'q' * 44
payload2.allowed_ips = ['10.10.0.4/32']

response = connection.wireguard.peers.config('wg0').update_bulk(
    [payload1, payload2]
)

print(type(response))
print(response)
