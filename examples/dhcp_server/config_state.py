from examples.config import connection
from ponika.config import DhcpConfig, PonikaConfig

ipv4_lease = connection.dhcp.static_leases_ipv4.create_model()
ipv4_lease.name = 'example-v4'
ipv4_lease.mac = 'AA:BB:CC:DD:EE:FF'
ipv4_lease.ip = '192.168.1.150'

ipv6_lease = connection.dhcp.static_leases_ipv6.create_model()
ipv6_lease.name = 'example-v6'
ipv6_lease.duid = '0001000123456789aabbccddeeff'
ipv6_lease.hostid = '150'

desired_config = PonikaConfig(
    dhcp=DhcpConfig(
        static_leases_ipv4=[ipv4_lease],
        static_leases_ipv6=[ipv6_lease],
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
