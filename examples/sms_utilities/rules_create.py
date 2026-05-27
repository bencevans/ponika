from examples.config import connection
from ponika.endpoints.sms_utilities.enums import (
    SmsRuleAction,
    SmsRuleAllowedPhone,
    SmsRuleAuthorization,
)
from ponika.endpoints.sms_utilities.rules import SmsRuleCreatePayload

payload = SmsRuleCreatePayload()
payload.enabled = True
payload.action = SmsRuleAction.VPN_STATUS
payload.smstext = 'apiexample'
payload.authorization = SmsRuleAuthorization.PASSWORD
payload.allowed_phone = SmsRuleAllowedPhone.ALL

response = connection.sms_utilities.rules.create(payload)

print(type(response))
print(response)
