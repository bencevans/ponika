from examples.config import connection

response = connection.recipients.email_users.upload_ca_certificate(
    item_id='example_id',
    file_path='/path/to/ca.pem',
)

print(type(response))
print(response)
