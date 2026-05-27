from examples.config import connection

response = connection.recipients.email_users.get_config()

print(type(response))
print(response)
