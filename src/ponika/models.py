from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class TeltonikaApiError(BaseModel):
    """Custom exception for Teltonika API errors."""

    code: int
    error: str
    source: str
    section: str

    def __str__(self) -> str:
        return f"Error {self.code}: {self.error} ({self.source}, {self.section})"


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: None | T = None
    errors: Optional[List[TeltonikaApiError]] = None


class Token(BaseModel):
    """Data model for token storage."""

    token: str
    expires_at: int
