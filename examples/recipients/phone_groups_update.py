from examples.config import connection

target_endpoint = connection.recipients.phone_groups
response = target_endpoint.get_config()

if len(response) == 0:
    print('No Phone Group found')
else:
    first_item = response[0]

    update_payload = target_endpoint.config_to_update_payload(first_item)

    update_payload.name = 'admins-updated'
    update_payload.tel = ['+49123456789']

    response = connection.recipients.phone_groups.update(update_payload)

    print(type(response))
    print(response)
