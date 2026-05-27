from examples.config import connection

target_endpoint = connection.dhcp.server_ipv6

response = target_endpoint.get_config()

if len(response) == 0:
    print('No DHCP IPv4 server configs found')
else:
    update_item = response[0]
    print(f'Update DHCP IPv4 server config with id {update_item.id}')

    update_payload = target_endpoint.config_to_update_payload(update_item)

    # Example change: toggle force flag if available
    if update_payload.force is True:
        update_payload.force = False
    else:
        update_payload.force = True

    response = target_endpoint.update(update_payload)

    print(type(response))
    print(response)
