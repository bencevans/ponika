from examples.config import connection

response = connection.users.get_config()

update_user = None

for user in response:
    if user.username != 'admin':
        update_user = user
        break

if update_user is None:
    print('This example cannot update admin user')
else:
    print(f'Update user {update_user.username} with id {update_user.id}')

    update_user_payload = connection.users.config_to_update_payload(
        update_user
    )

    update_user_payload.group = 'new_group'

    response = connection.users.update(update_user_payload)

    print(type(response))
    print(response)
