from examples.config import connection

response = connection.zerotier.config.get_config()

print(type(response))
print(response)
