from examples.config import connection

response = connection.recipients.phone_groups.upload_phone_numbers(
    item_id='example_id',
    file_path='/path/to/phone_numbers.txt',
)

print(type(response))
print(response)
