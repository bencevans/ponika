from examples.config import connection


response = connection.ip_routes.routes_ipv6.get_config()

print(type(response))
print(response)
