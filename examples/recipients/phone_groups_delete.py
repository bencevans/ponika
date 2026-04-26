from examples.config import connection

target_endpoint = connection.recipients.phone_groups
response = target_endpoint.get_config()

if len(response) == 0:
    print('No Phone Group found')
else:
    first_item = response[0]

    update_payload = target_endpoint.delete(first_item.id)
