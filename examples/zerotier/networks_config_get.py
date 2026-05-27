from examples.config import connection

response = connection.zerotier.networks.config('1').get_config()

response = connection.zerotier.networks.config('1').get_config(response[0].id)

print(type(response))
print(response)
