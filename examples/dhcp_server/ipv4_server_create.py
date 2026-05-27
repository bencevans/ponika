from examples.config import connection
from ponika.endpoints.dhcp.enums import DHCPMode

target_endpoint = connection.dhcp.server_ipv4

# This example shows how to create a DHCP Server
# This is a theoretical case, because you cannot delete the existing one

newInterface = target_endpoint.create_model(id='lan')
# newInterface.interface = "lan"
newInterface.mode = DHCPMode.SERVER
newInterface.start_ip = '10.10.3.100'
newInterface.end_ip = '10.10.3.200'
newInterface.leasetime = '6h'

response = connection.dhcp.server_ipv4.create(newInterface)

print(type(response))
print(response)
