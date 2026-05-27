from examples.config import connection


response = connection.users.get_config('cfg02f8be')

print(type(response))
print(response)
