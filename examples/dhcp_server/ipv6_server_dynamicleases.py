from examples.config import connection

target_endpoint = connection.dhcp.server_ipv6

response = target_endpoint.get_dynamic_leases()

print(type(response))
print(response)
