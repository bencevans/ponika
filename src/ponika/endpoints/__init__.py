from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    List,
    Type,
    TypeVar,
    cast,
    get_origin,
    overload,
)

from pydantic import ValidationError

from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel, BasePayload

if TYPE_CHECKING:
    from ponika import PonikaClient


TItemCreatePayload = TypeVar('TItemCreatePayload', bound=BasePayload)
TItemUpdatePayload = TypeVar('TItemUpdatePayload', bound=BasePayload)

TConfigResponse = TypeVar('TConfigResponse', bound=BaseModel)
TDeleteResponse = TypeVar('TDeleteResponse', bound=BaseModel)
TStatusResponseModel = TypeVar('TStatusResponseModel', bound=BaseModel)


class Endpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client


class StatusEndpoint(Generic[TStatusResponseModel]):
    status_response_model = Type[TStatusResponseModel]
    allow_status_without_id: bool = True
    allow_status_with_id: bool = True

    @overload
    def get_status(self, item_id: int | str) -> TStatusResponseModel: ...

    @overload
    def get_status(self) -> List[TStatusResponseModel]: ...

    def get_status(
        self, item_id: int | str | None = None
    ) -> List[TStatusResponseModel] | TStatusResponseModel:
        """Fetch wireless interfaces status from the device."""
        if item_id is None and not self.allow_status_without_id:
            raise ValueError(
                f'{self.__class__.__name__}.get_status() without item_id is not available for this endpoint.'
            )

        if item_id is not None and not self.allow_status_with_id:
            raise ValueError(
                f'{self.__class__.__name__}.get_status(item_id=...) is not available for this endpoint.'
            )

        endpoint = (
            f'{self.status_endpoint_path}/{item_id}'
            if item_id
            else f'{self.status_endpoint_path}'
        )
        ResultType = (
            self.status_response_model
            if item_id
            else List[self.status_response_model]
        )

        response = self._client._get(endpoint)
        try:
            response_obj = ApiResponse[ResultType].model_validate(response)
        except ValidationError as e:
            print(f'Error during request: GET {endpoint}')
            print(
                f'Error during response validation to class ApiResponse[{ResultType}]'
            )
            print(f'Response we got: {response}')
            raise e

        if not response_obj.success:
            raise TeltonikaApiException(response_obj.errors)

        return response_obj.data


class DeleteEndpoint(Generic[TDeleteResponse]):
    delete_reponse_model = Type[TDeleteResponse]
    allow_bulk_delete: bool = False
    bulk_delete_endpoint_path: str | None = None
    bulk_delete_response_model: Any | None = None

    def delete(self, item_id: str | int) -> TDeleteResponse:
        response = self._client._delete(
            endpoint=f'{self.endpoint_path}/{item_id}',
            data_model=self.delete_reponse_model,
        )
        if not response.success:
            raise TeltonikaApiException(response.errors)

        return cast(TDeleteResponse, response.data)

    def delete_bulk(self, item_ids: List[str | int]) -> List[TDeleteResponse]:
        if not self.allow_bulk_delete:
            raise ValueError(
                f'{self.__class__.__name__}.delete_bulk() is not available '
                'for this endpoint.'
            )

        endpoint = self.bulk_delete_endpoint_path or self.endpoint_path
        response_data_model = (
            self.bulk_delete_response_model or self.delete_reponse_model
        )

        response_model = (
            response_data_model
            if get_origin(response_data_model) is list
            else List[response_data_model]
        )

        response = self._client._delete(
            endpoint=endpoint,
            data_model=response_model,
            params={'data': item_ids},
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return cast(List[TDeleteResponse], response.data)


class CreateEndpoint(Generic[TItemCreatePayload, TConfigResponse]):
    config_response_model = Type[TConfigResponse]

    def create(self, payload: TItemCreatePayload) -> TConfigResponse:
        response = self._client._post_data(
            endpoint=self.endpoint_path,
            params=payload,
            data_model=self.config_response_model,
        )
        if not response.success:
            raise TeltonikaApiException(response.errors)
        return response.data


class UpdateEndpoint(Generic[TItemUpdatePayload, TConfigResponse]):
    config_response_model = Type[TConfigResponse]
    update_model: Type[TItemUpdatePayload]
    allow_bulk_update: bool = False
    bulk_update_strip_item_id: bool = True
    bulk_endpoint_path: str | None = None

    def update_by_id(
        self,
        item_id: str | int,
        payload: TItemUpdatePayload | dict,
    ) -> TConfigResponse:
        response = self._client._put_data(
            endpoint=f'{self.endpoint_path}/{item_id}',
            params=payload,
            data_model=self.config_response_model,
        )
        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)
        return response.data

    def update(self, payload: TItemUpdatePayload) -> TConfigResponse:
        item_id = getattr(payload, 'id', None)
        if item_id is None:
            raise ValueError(
                f'{self.__class__.__name__}.update() requires payload.id; '
                'use update_by_id(item_id, payload) when id is not part '
                'of payload.'
            )

        item_data = payload.asdict()
        item_data.pop('id', None)
        return self.update_by_id(item_id=item_id, payload=item_data)

    def update_bulk(
        self,
        payloads: List[TItemUpdatePayload],
    ) -> List[TConfigResponse]:
        if not self.allow_bulk_update:
            raise ValueError(
                f'{self.__class__.__name__}.update_bulk() is not available '
                'for this endpoint.'
            )

        data = []
        for payload in payloads:
            item_data = payload.asdict()
            if self.bulk_update_strip_item_id:
                item_data.pop('id', None)
            data.append(item_data)

        endpoint = self.bulk_endpoint_path or self.endpoint_path
        response = self._client._put(
            endpoint=endpoint,
            data_model=object,
            params={'data': data},
        )

        response_model = ApiResponse[List[self.config_response_model]]
        response_obj = response_model.model_validate(
            response.model_dump(mode='python')
        )

        if not response_obj.success or response_obj.data is None:
            raise TeltonikaApiException(response_obj.errors)
        return cast(List[TConfigResponse], response_obj.data)

    def config_to_update_payload(self, payload: TConfigResponse):
        return self.update_model(**payload.model_dump(mode='python'))

        # target_fields = self.update_model.model_fields.keys()
        # target_fields = [field.name for field in fields(self.update_model)]

        # data = payload.model_dump(include=target_fields)
        # return self.update_model(**data)


class ReadEndpoint(Generic[TConfigResponse]):
    _client: 'PonikaClient'
    endpoint_path: str
    config_response_model = Type[TConfigResponse]

    @overload
    def get_config(self, item_id: int | str) -> TConfigResponse: ...

    @overload
    def get_config(self) -> List[TConfigResponse]: ...

    def get_config(
        self,
        item_id: str | int | None = None,
    ) -> List[TConfigResponse] | TConfigResponse:
        endpoint = (
            f'{self.endpoint_path}/{item_id}'
            if item_id
            else self.endpoint_path
        )

        response_model = (
            ApiResponse[self.config_response_model]
            if item_id
            else ApiResponse[list[self.config_response_model]]
        )

        response = self._client._get(endpoint)

        response = response_model.model_validate(response)

        if not response.success:
            raise TeltonikaApiException(response.errors)
        return cast(List[TConfigResponse] | TConfigResponse, response.data)


class CRUDEndpoint(
    Endpoint,
    CreateEndpoint[TItemCreatePayload, TConfigResponse],
    ReadEndpoint[TConfigResponse],
    UpdateEndpoint[TItemUpdatePayload, TConfigResponse],
    DeleteEndpoint[TDeleteResponse],
    Generic[
        TItemCreatePayload,
        TConfigResponse,
        TItemUpdatePayload,
        TDeleteResponse,
    ],
):
    endpoint_path: str
    create_model: Type[TItemCreatePayload]
    config_id_field: str = 'id'
    config_match_fields: tuple[str, ...] = ('id', 'name')


class DynamicPathCRUDEndpoint(
    CRUDEndpoint[
        TItemCreatePayload,
        TConfigResponse,
        TItemUpdatePayload,
        TDeleteResponse,
    ],
    Generic[
        TItemCreatePayload,
        TConfigResponse,
        TItemUpdatePayload,
        TDeleteResponse,
    ],
):
    """CRUDEndpoint variant that formats endpoint_path from runtime params."""

    endpoint_path_template: str

    def __init__(
        self,
        client: 'PonikaClient',
        **path_params: str | int,
    ) -> None:
        super().__init__(client)
        self._path_params = path_params

    @property
    def endpoint_path(self) -> str:  # type: ignore[override]
        return self.endpoint_path_template.format(**self._path_params)
