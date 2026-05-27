from examples.config import connection
from ponika.endpoints.zerotier.networks import (
    ZerotierNetworkConfigUpdatePayload,
)

response = connection.zerotier.networks.config('1').get_config()

payload = ZerotierNetworkConfigUpdatePayload(id=response[0].id)
payload.enabled = False
payload.name = 'office_backup'
payload.allow_default = False

response = connection.zerotier.networks.config('1').update(payload)

print(type(response))
print(response)
