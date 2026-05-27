from examples.config import connection

target_endpoint = connection.dhcp.static_leases_ipv6

create_payload = target_endpoint.create_model()
create_payload.name = 'example.com'
create_payload.duid = '00010001293abc12001122334455'
create_payload.hostid = '0010'

response = target_endpoint.create(create_payload)

print(type(response))
print(response)
