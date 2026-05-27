from ponika.endpoints import Endpoint
from ponika.exceptions import TeltonikaApiException
from ponika.models import BaseModel


class GenerateKeysResponse(BaseModel):
    private: str
    public: str


class ActionsEndpoint(Endpoint):
    def post_generate_keys(self) -> GenerateKeysResponse:
        response = self._client._post(
            endpoint='/wireguard/actions/generate_keys',
            data_model=GenerateKeysResponse,
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data
