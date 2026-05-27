from examples.config import connection
from ponika.endpoints.sms_utilities.enums import (
    SmsRuleAction,
    SmsRuleAllowedPhone,
    SmsRuleAuthorization,
)

target_endpoint = connection.sms_utilities.rules
response = target_endpoint.get_config()

if len(response) == 0:
    print('No SMS utilities rules found')
else:
    first_item = None
    for item in response:
        if item.smstext == 'apiexample':
            first_item = item
            break

    if first_item is None:
        print('No SMS utilities with smstext apiexample found to update')
    else:
        update_payload = target_endpoint.config_to_update_payload(first_item)
        update_payload.enabled = False
        update_payload.action = SmsRuleAction.REBOOT
        update_payload.authorization = SmsRuleAuthorization.LOCAL
        update_payload.password = 'YYn&vt]-4gZvP:D6'
        update_payload.allowed_phone = SmsRuleAllowedPhone.SINGLE
        update_payload.tel = '+49123456789'

        response = target_endpoint.update(update_payload)

        print(type(response))
        print(response)
