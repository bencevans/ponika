from examples.config import connection

target_endpoint = connection.dhcp.static_leases_ipv4

response = target_endpoint.get_config()

if len(response) == 0:
    print('No DHCP static IPv4 leases found')
else:
    first_item = response[0]
    response = target_endpoint.get_config(first_item.id)

    print(type(response))
    print(response)
