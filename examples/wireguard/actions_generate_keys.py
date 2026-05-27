from examples.config import connection

response = connection.wireguard.actions.post_generate_keys()

print(type(response))
print(response)
