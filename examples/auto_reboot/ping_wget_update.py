from examples.config import connection
from ponika.endpoints.auto_reboot.enums import PingWgetActionWhen, PingWgetType

target_endpoint = connection.auto_reboot.ping_wget
response = target_endpoint.get_config()

if len(response) == 0:
    print('No Auto Reboot ping/wget configs found')
else:
    first_item = response[0]
    response = target_endpoint.get_config(first_item.id)

    update_payload = connection.auto_reboot.ping_wget.config_to_update_payload(
        response
    )

    update_payload.enable = False
    update_payload.type = PingWgetType.WGET
    update_payload.action_when = PingWgetActionWhen.ANY
    update_payload.host = ['https://example.com']

    response = connection.auto_reboot.ping_wget.update(update_payload)

    print(type(response))
    print(response)
