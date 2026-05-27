from examples.config import connection

target_endpoint = connection.dhcp.static_leases_ipv4

create_payload = target_endpoint.create_model()
create_payload.name = 'example.com'
create_payload.mac = 'AA:BB:CC:DD:EE:FF'
create_payload.ip = '192.168.1.150'

response = target_endpoint.create(create_payload)

print(type(response))
print(response)
