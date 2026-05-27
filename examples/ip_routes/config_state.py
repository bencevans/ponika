from examples.config import connection
from ponika.config import IpRoutesConfig, PonikaConfig
from ponika.endpoints.ip_routes.enums import RoutingType

ipv4_route = connection.ip_routes.routes_ipv4.create_model()
ipv4_route.interface = 'lan'
ipv4_route.target = '10.10.10.0'
ipv4_route.netmask = '255.255.255.0'
ipv4_route.gateway = '192.168.1.1'
ipv4_route.metric = '1'
ipv4_route.mtu = '1500'
ipv4_route.type = RoutingType.ANYCAST
ipv4_route.table = '254'

ipv6_route = connection.ip_routes.routes_ipv6.create_model()
ipv6_route.interface = 'lan'
ipv6_route.target = '2001:db8:10::/64'
ipv6_route.gateway = '2001:db8::1'
ipv6_route.metric = '1'
ipv6_route.mtu = '1500'
ipv6_route.type = RoutingType.ANYCAST
ipv6_route.table = '254'

desired_config = PonikaConfig(
    ip_routes=IpRoutesConfig(
        routes_ipv4=[ipv4_route],
        routes_ipv6=[ipv6_route],
    )
)

preview = connection.config.apply(
    desired_config,
    dry_run=True,
    delete_unmanaged=False,
)
print(preview.changes)

result = connection.config.apply(
    desired_config,
    delete_unmanaged=False,
)
print(result)
