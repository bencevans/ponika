from examples.config import connection

response = connection.zerotier.networks.config('1').delete('net1')

print(type(response))
print(response)
