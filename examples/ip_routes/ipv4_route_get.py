from examples.config import connection


response = connection.ip_routes.routes_ipv4.get_config('1')

print(type(response))
print(response)
