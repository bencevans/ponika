from ponika.endpoints import CRUDEndpoint
from ponika.endpoints.recipients.common import (
    DeleteResponse,
    UploadFileResponse,
)
from ponika.exceptions import TeltonikaApiException
from ponika.models import BaseModel, BasePayload


class EmailUserBase:
    name: str
    secure_conn: bool | None = None
    smtp_ip: str | None = None
    smtp_port: str | None = None
    credentials: bool | None = None
    username: str | None = None
    senderemail: str | None = None
    do_not_verify: bool | None = None
    ca_file: str | None = None


class EmailUserPayloadBase(EmailUserBase):
    password: str | None = None


class EmailUserConfigResponse(BaseModel, EmailUserBase):
    id: str


class EmailUserCreatePayload(BasePayload, EmailUserPayloadBase):
    pass


class EmailUserUpdatePayload(BasePayload, EmailUserPayloadBase):
    id: str


class EmailTestPayload(BasePayload):
    smtp_ip: str
    smtp_port: str
    senderemail: str
    secure_conn: bool
    username: str | None = None
    password: str | None = None


class EmailUsersEndpoint(
    CRUDEndpoint[
        EmailUserCreatePayload,
        EmailUserConfigResponse,
        EmailUserUpdatePayload,
        DeleteResponse,
    ]
):
    endpoint_path = '/recipients/email_users/config'

    config_response_model = EmailUserConfigResponse
    create_model = EmailUserCreatePayload
    update_model = EmailUserUpdatePayload
    delete_reponse_model = DeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True

    def send_test_email(self, payload: EmailTestPayload) -> None:
        response = self._client._post_data(
            endpoint='/recipients/email_users/actions/send_email',
            data_model=object,
            params=payload,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return None

    def upload_ca_certificate(
        self, item_id: str | int, file_path: str
    ) -> UploadFileResponse:
        response = self._client._post_files(
            endpoint=f'{self.endpoint_path}/{item_id}',
            data_model=UploadFileResponse,
            files={'file': file_path},
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data
