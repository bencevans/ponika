from examples.config import connection

target_endpoint = connection.sms_utilities.rules
response = target_endpoint.get_config()

if len(response) == 0:
    print('No SMS utilities rules found')
else:
    first_item = response[0]
    response = target_endpoint.get_config(first_item.id)

    print(type(response))
    print(response)
