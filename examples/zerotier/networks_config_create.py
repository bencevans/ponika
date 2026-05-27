from examples.config import connection
from ponika.endpoints.zerotier.networks import (
    ZerotierNetworkConfigCreatePayload,
)

payload = ZerotierNetworkConfigCreatePayload()
payload.enabled = True
payload.name = 'office'
payload.allow_managed = True
payload.allow_default = False
payload.allow_global = False
payload.network_id = '8d2e657774097d36'

response = connection.zerotier.networks.config('1').create(payload)

print(type(response))
print(response)
