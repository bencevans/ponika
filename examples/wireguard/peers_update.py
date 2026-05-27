from examples.config import connection
from ponika.endpoints.wireguard.peers import WireguardPeerUpdateItemPayload

payload = WireguardPeerUpdateItemPayload(id='peer1')
payload.public_key = 'p' * 44
payload.allowed_ips = ['10.10.0.3/32']
payload.route_allowed_ips = False

response = connection.wireguard.peers.config('wg0').update(payload)

print(type(response))
print(response)
