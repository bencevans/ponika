from typing import List

from ponika.endpoints import CRUDEndpoint
from ponika.endpoints.recipients.common import (
    DeleteResponse,
    UploadFileResponse,
)
from ponika.exceptions import TeltonikaApiException
from ponika.models import BaseModel, BasePayload


class PhoneGroupBase:
    name: str
    tel: List[str] | None = None


class PhoneGroupConfigResponse(BaseModel, PhoneGroupBase):
    id: str


class PhoneGroupCreatePayload(BasePayload, PhoneGroupBase):
    pass


class PhoneGroupUpdatePayload(BasePayload, PhoneGroupBase):
    id: str


class PhoneGroupsEndpoint(
    CRUDEndpoint[
        PhoneGroupCreatePayload,
        PhoneGroupConfigResponse,
        PhoneGroupUpdatePayload,
        DeleteResponse,
    ]
):
    endpoint_path = '/recipients/phone_groups/config'

    config_response_model = PhoneGroupConfigResponse
    create_model = PhoneGroupCreatePayload
    update_model = PhoneGroupUpdatePayload
    delete_reponse_model = DeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True

    def upload_phone_numbers(
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
