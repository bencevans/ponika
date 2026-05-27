from examples.config import connection

response = connection.zerotier.networks.config('1').get_config()

print(type(response))
print(response)
