from examples.config import connection
from ponika.endpoints.ip_routes.enums import RoutingType


new_route = connection.ip_routes.routes_ipv6.create_model()
new_route.interface = 'wan'
new_route.target = '2001:db8:1::'
new_route.gateway = 'fe80::1'
new_route.metric = '1'
new_route.mtu = '1500'
new_route.type = RoutingType.UNICAST
new_route.table = '254'

response = connection.ip_routes.routes_ipv6.create(new_route)

print(type(response))
print(response)
