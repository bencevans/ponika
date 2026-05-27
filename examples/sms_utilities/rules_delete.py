from examples.config import connection

target_endpoint = connection.sms_utilities.rules
response = target_endpoint.get_config()

if len(response) == 0:
    print('No SMS utilities rules found')
else:
    first_item = None
    for item in response:
        if item.smstext == 'apiexample':
            first_item = item
            break

    if first_item is None:
        print('No SMS utilities with smstext apiexample found to update')
    else:
        target_endpoint.delete(first_item.id)
