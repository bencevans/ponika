from examples.config import connection
from ponika.endpoints.recipients.phone_groups import PhoneGroupCreatePayload

payload = PhoneGroupCreatePayload(
    name='admins',
    tel=['+49123456'],
)

response = connection.recipients.phone_groups.create(payload)

print(type(response))
print(response)
