from examples.config import connection


response = connection.users.get_config()

delete_user = None

for user in response:
    if user.username != 'admin':
        delete_user = user
        break

if delete_user is None:
    print('This example cannot delete admin user')
else:
    print(f'Delete user {delete_user.username} with id {delete_user.id}')

    response = connection.users.delete(delete_user.id)

    print(type(response))
    print(response)
