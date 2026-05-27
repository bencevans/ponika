from examples.config import connection
from ponika.endpoints.zerotier.config import ZerotierConfigCreatePayload

payload = ZerotierConfigCreatePayload()
payload.enabled = True
payload.name = 'main_zt'

response = connection.zerotier.config.create(payload)

print(type(response))
print(response)
