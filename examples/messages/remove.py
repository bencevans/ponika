from examples.config import connection

response = connection.messages.remove(
    modem_id='1-1',
    sms_ids=['0'],
)

print(type(response))
print(response)
