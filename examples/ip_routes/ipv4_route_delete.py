from examples.config import connection


response = connection.ip_routes.routes_ipv4.get_config()

delete_route = None

for route in response:
    delete_route = route
    break

if delete_route is None:
    print('No IPv4 route found to delete')
else:
    print(f'Delete IPv4 route with id {delete_route.id}')

    response = connection.ip_routes.routes_ipv4.delete(delete_route.id)

    print(type(response))
    print(response)
