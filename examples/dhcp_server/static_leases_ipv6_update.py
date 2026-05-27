from examples.config import connection

target_endpoint = connection.dhcp.static_leases_ipv6

response = target_endpoint.get_config()

if len(response) == 0:
    print('No DHCP static IPv6 leases found')
else:
    update_item = response[0]
    update_payload = target_endpoint.config_to_update_payload(update_item)

    update_payload.name = 'newname-example.com'

    response = target_endpoint.update(update_payload)

    print(type(response))
    print(response)
