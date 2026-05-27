import pprint
from examples.config import connection

import secrets


password = secrets.token_urlsafe(16)

newInterface = connection.users.create_model(
    username='new_username', password=password, group='admin', ssh_enable=False
)

response = connection.users.create(newInterface)

print(f'### Created User with password: {password}')

print(type(response))
pprint.pprint(response)
