from typing import TYPE_CHECKING

from ponika.endpoints.recipients.email_users import EmailUsersEndpoint
from ponika.endpoints.recipients.phone_groups import PhoneGroupsEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class RecipientsEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client
        self.phone_groups = PhoneGroupsEndpoint(client)
        self.email_users = EmailUsersEndpoint(client)
