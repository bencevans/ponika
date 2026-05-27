from examples.config import connection
from ponika.config import PonikaConfig, RecipientsConfig, SmsUtilitiesConfig
from ponika.endpoints.recipients.phone_groups import PhoneGroupCreatePayload
from ponika.endpoints.sms_utilities.enums import (
    SmsRuleAction,
    SmsRuleAllowedPhone,
    SmsRuleAuthorization,
)
from ponika.endpoints.sms_utilities.rules import SmsRuleCreatePayload


def print_changes(preview):
    print('Planned changes:')
    for change in preview.changes:
        print(
            f'- {change.action.value}: '
            f'{change.section} {change.match_field}={change.match_value}'
        )
        print(f'  Existing: {change.existing}')
        print(f'  Desired:  {change.desired}')

    result = connection.config.apply(
        desired_config,
        delete_unmanaged=False,
    )

    print(f'Created: {len(result.created)}')
    print(f'Updated: {len(result.updated)}')
    print(f'Deleted: {len(result.deleted)}')
    print(f'Unchanged: {len(result.unchanged)}')


smsRuleVpnStatusPayload = SmsRuleCreatePayload()
smsRuleVpnStatusPayload.enabled = True
smsRuleVpnStatusPayload.action = SmsRuleAction.VPN_STATUS
smsRuleVpnStatusPayload.smstext = 'apiexample'
smsRuleVpnStatusPayload.authorization = SmsRuleAuthorization.PASSWORD
smsRuleVpnStatusPayload.allowed_phone = SmsRuleAllowedPhone.ALL

desired_config = PonikaConfig(
    recipients=RecipientsConfig(
        phone_groups=[
            PhoneGroupCreatePayload(name='admins', tel=['+49123456'])
        ]
    ),
    sms_utilities=SmsUtilitiesConfig(rules=[smsRuleVpnStatusPayload]),
)

preview = connection.config.apply(
    desired_config,
    dry_run=True,
    delete_unmanaged=False,
)

print_changes(preview)


result = connection.config.apply(
    desired_config,
    delete_unmanaged=False,
)

print(f'Created: {len(result.created)}')
print(f'Updated: {len(result.updated)}')
print(f'Deleted: {len(result.deleted)}')
print(f'Unchanged: {len(result.unchanged)}')
