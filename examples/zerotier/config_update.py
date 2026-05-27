from examples.config import connection
from ponika.endpoints.zerotier.config import ZerotierConfigUpdatePayload

payload = ZerotierConfigUpdatePayload(id='1')
payload.enabled = False
payload.name = 'zt_updated'

response = connection.zerotier.config.update(payload)

print(type(response))
print(response)
