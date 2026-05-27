from examples.config import connection


response = connection.users.get_config()

print(type(response))
print(response)
