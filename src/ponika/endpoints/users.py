from typing import TYPE_CHECKING, Optional
from ponika.endpoints import CRUDEndpoint
from ponika.models import BaseModel, BasePayload

if TYPE_CHECKING:
    pass


class UserDeleteResponse(BaseModel):
    id: str


class UserDefinition(BasePayload):
    username: str
    password: str
    group: str
    ssh_enable: bool = False


class UserConfigResponse(BaseModel):
    id: str
    username: str
    group: str
    ssh_enable: bool


class UserUpdateDefinition(BasePayload):
    id: str
    group: Optional[str] = ''
    ssh_enable: Optional[bool] = False

    current_password: Optional[str] = None
    password: Optional[str] = None
    password_confirm: Optional[str] = None


class UsersEndpoint(
    CRUDEndpoint[
        UserDefinition,
        UserConfigResponse,
        UserUpdateDefinition,
        UserDeleteResponse,
    ]
):
    endpoint_path = '/users/config'

    create_model = UserDefinition
    update_model = UserUpdateDefinition

    config_response_model = UserConfigResponse
    delete_reponse_model = UserDeleteResponse
    config_match_fields = ('id', 'username')
