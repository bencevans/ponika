from examples.config import connection

response = connection.wireguard.config.get_config()

print(type(response))
print(response)
