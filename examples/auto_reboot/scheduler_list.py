from examples.config import connection

response = connection.auto_reboot.scheduler.get_config()

print(type(response))
print(response)
