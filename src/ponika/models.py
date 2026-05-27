from enum import Enum
from typing import TYPE_CHECKING, Any, Generic, List, Optional, TypeVar

if TYPE_CHECKING:
    pass

from pydantic import BaseModel as PydanticBaseModel, ConfigDict


T = TypeVar('T')


class BasePayload(PydanticBaseModel):
    def asdict(self) -> dict[str, Any]:
        def convert(value: Any) -> Any:
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, list):
                return [convert(v) for v in value]
            if isinstance(value, bool):
                return '1' if value is True else '0'
            if isinstance(value, dict):
                return {k: convert(v) for k, v in value.items()}

            return value

        response = self.model_dump(exclude_none=True, by_alias=True)
        return convert(response)


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(frozen=True)


class TeltonikaApiError(BaseModel):
    """Custom exception for Teltonika API errors."""

    code: int
    error: str
    source: str | int
    section: Optional[str] = None

    def __str__(self) -> str:
        return (
            f'Error {self.code}: {self.error} ({self.source}, {self.section})'
        )


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: None | T = None
    errors: Optional[List[TeltonikaApiError]] = None


class Token(BaseModel):
    """Data model for token storage."""

    token: str
    expires_at: int
