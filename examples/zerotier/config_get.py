from examples.config import connection

response = connection.zerotier.config.get_config('1')

print(type(response))
print(response)
