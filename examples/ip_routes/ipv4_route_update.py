from examples.config import connection


response = connection.ip_routes.routes_ipv4.get_config()

update_route = None

for route in response:
    update_route = route
    break

if update_route is None:
    print('No IPv4 route found to update')
else:
    print(f'Update IPv4 route with id {update_route.id}')

    update_route_payload = (
        connection.ip_routes.routes_ipv4.config_to_update_payload(update_route)
    )

    update_route_payload.metric = '2'

    response = connection.ip_routes.routes_ipv4.update(update_route_payload)

    print(type(response))
    print(response)
