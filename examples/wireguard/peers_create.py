from examples.config import connection
from ponika.endpoints.wireguard.peers import WireguardPeerCreateItemPayload

payload = WireguardPeerCreateItemPayload(id='peer1')
payload.public_key = 'p' * 44
payload.allowed_ips = ['10.10.0.2/32']
payload.route_allowed_ips = True

response = connection.wireguard.peers.config('wg0').create(payload)

print(type(response))
print(response)
