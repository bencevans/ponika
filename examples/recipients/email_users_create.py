from examples.config import connection
from ponika.endpoints.recipients.email_users import EmailUserCreatePayload

payload = EmailUserCreatePayload(
    name='alerts',
    secure_conn=True,
    smtp_ip='smtp.example.com',
    smtp_port='587',
    credentials=True,
    username='alerts',
    password='secret',
    senderemail='alerts@example.com',
    do_not_verify=False,
)

response = connection.recipients.email_users.create(payload)

print(type(response))
print(response)
