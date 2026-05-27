from examples.config import connection

target_endpoint = connection.dhcp.server_ipv4

response = target_endpoint.get_config()

print(type(response))
print(response)
