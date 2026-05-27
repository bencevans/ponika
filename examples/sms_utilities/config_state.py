from examples.config import connection
from ponika.config import PonikaConfig, SmsUtilitiesConfig
from ponika.endpoints.sms_utilities.enums import (
    SmsRuleAction,
    SmsRuleAllowedPhone,
    SmsRuleAuthorization,
)
from ponika.endpoints.sms_utilities.rules import SmsRuleCreatePayload

rule = SmsRuleCreatePayload()
rule.enabled = True
rule.action = SmsRuleAction.VPN_STATUS
rule.smstext = 'apiexample'
rule.authorization = SmsRuleAuthorization.PASSWORD
rule.allowed_phone = SmsRuleAllowedPhone.ALL

desired_config = PonikaConfig(sms_utilities=SmsUtilitiesConfig(rules=[rule]))

preview = connection.config.apply(
    desired_config,
    dry_run=True,
    delete_unmanaged=False,
)
print(preview.changes)

result = connection.config.apply(
    desired_config,
    delete_unmanaged=False,
)
print(result)
