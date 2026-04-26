from examples.config import connection
from ponika.endpoints.recipients.email_users import EmailTestPayload

payload = EmailTestPayload(
    smtp_ip='smtp.example.com',
    smtp_port='587',
    senderemail='alerts@example.com',
    secure_conn=True,
)

response = connection.recipients.email_users.send_test_email(payload)

print(type(response))
print(response)
