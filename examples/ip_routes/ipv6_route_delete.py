from examples.config import connection


response = connection.ip_routes.routes_ipv6.get_config()

delete_route = None

for route in response:
    delete_route = route
    break

if delete_route is None:
    print('No IPv6 route found to delete')
else:
    print(f'Delete IPv6 route with id {delete_route.id}')

    response = connection.ip_routes.routes_ipv6.delete(delete_route.id)

    print(type(response))
    print(response)
