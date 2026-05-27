from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ValidationError
from typing import TYPE_CHECKING

from ponika.exceptions import TeltonikaApiException
from ponika.models import TeltonikaApiError

if TYPE_CHECKING:
    from ponika import PonikaClient


class DataUsagesApiResponse(BaseModel):
    success: bool
    errors: Optional[List[TeltonikaApiError]] = None

    data: List[List[int]] | None = None


class UsageInterval(str, Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    TOTAL = 'total'
    # CUSTOM = "custom"


class DataUsageEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client

    # , custom_from_timestamp: int | None = None, custom_to_timestamp: int | None = None
    # "custom" is not supported
    def get_simcard_usage(self, interval: UsageInterval) -> List[List[int]]:
        """https://developers.teltonika-networks.com/reference/rut241/7.20/v1.12/data-usage#get-data_usage-interval-status"""

        endpoint = f'/data_usage/{interval.value}/status'  # if interval is not UsageInterval.CUSTOM else f"/data_usage/{interval}/status?from={custom_from_timestamp}&to={custom_to_timestamp}"
        response = self._client._get(endpoint)

        try:
            response_obj = DataUsagesApiResponse.model_validate(response)
        except ValidationError as e:
            print(f'Error during request: GET {endpoint}')
            print(
                f'Error during response validation to class ApiResponse[{DataUsagesApiResponse}]'
            )
            print(f'Response we got: {response}')
            raise e

        if not response_obj.success or response_obj.data is None:
            raise TeltonikaApiException(response_obj.errors)

        return response_obj.data
