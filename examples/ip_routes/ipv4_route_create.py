from examples.config import connection
from ponika.endpoints.ip_routes.enums import RoutingType


new_route = connection.ip_routes.routes_ipv4.create_model()
new_route.interface = 'lan'
new_route.target = '10.10.10.0'
new_route.netmask = '255.255.255.0'
new_route.gateway = '192.168.1.1'
new_route.metric = '1'
new_route.mtu = '1500'
new_route.type = RoutingType.ANYCAST
new_route.table = '254'

response = connection.ip_routes.routes_ipv4.create(new_route)

print(type(response))
print(response)
