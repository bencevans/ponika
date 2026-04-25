from examples.config import connection

target_endpoint = connection.auto_reboot.ping_wget

response = target_endpoint.get_config()

print(type(response))
print(response)
