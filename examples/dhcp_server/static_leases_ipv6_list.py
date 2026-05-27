from examples.config import connection

target_endpoint = connection.dhcp.static_leases_ipv6

response = target_endpoint.get_config()

print(type(response))
print(response)
