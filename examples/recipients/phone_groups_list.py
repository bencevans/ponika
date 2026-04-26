from examples.config import connection

response = connection.recipients.phone_groups.get_config()

print(type(response))
print(response)
