from examples.config import connection

target_endpoint = connection.recipients.email_users
response = target_endpoint.get_config()

if len(response) == 0:
    print('No Email Users rules found')
else:
    first_item = response[0]

    update_payload = target_endpoint.config_to_update_payload(first_item)

    update_payload.senderemail = 'updates@example-domain.com'
    update_payload.name = 'alerts-update'

    response = target_endpoint.update(update_payload)

    print(type(response))
    print(response)
