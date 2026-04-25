from examples.config import connection

target_endpoint = connection.auto_reboot.scheduler
response = target_endpoint.get_config()

if len(response) == 0:
    print('No Auto Reboot Scheduler configs found')
else:
    first_item = response[0]
    response = target_endpoint.get_config(first_item.id)

    print(type(response))
    print(response)
