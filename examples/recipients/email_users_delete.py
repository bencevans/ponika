from examples.config import connection

target_endpoint = connection.recipients.email_users
response = target_endpoint.get_config()

if len(response) == 0:
    print('No Email Users rules found')
else:
    first_item = response[0]

    response = target_endpoint.delete(first_item.id)

    print(type(response))
    print(response)
