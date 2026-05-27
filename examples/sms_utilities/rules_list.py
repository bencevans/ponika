from examples.config import connection

response = connection.sms_utilities.rules.get_config()

print(type(response))
print(response)
