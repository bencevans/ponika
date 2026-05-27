from examples.config import connection

from ponika.config import PonikaConfig, RecipientsConfig
from ponika.endpoints.recipients.email_users import EmailUserCreatePayload
from ponika.endpoints.recipients.phone_groups import PhoneGroupCreatePayload

phone_group = PhoneGroupCreatePayload()
phone_group.name = 'admins 123'
phone_group.tel = ['+49123456']

email_user = EmailUserCreatePayload()
email_user.name = 'alerts'
email_user.secure_conn = True
email_user.smtp_ip = 'smtp.example.com'
email_user.smtp_port = '587'
email_user.credentials = True
email_user.username = 'alerts'
email_user.password = 'secret'
email_user.senderemail = 'alerts@example.com'
email_user.do_not_verify = False

desired_config = PonikaConfig(
    recipients=RecipientsConfig(
        phone_groups=[phone_group],
        email_users=[email_user],
    )
)

preview = connection.config.apply(
    desired_config,
    dry_run=True,
    delete_unmanaged=False,
)

connection.config.print_changes(preview)
