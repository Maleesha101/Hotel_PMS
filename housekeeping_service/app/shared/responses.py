"""Common API response models.

`ApiResponse` is a simple wrapper used for most endpoints. It includes a
`status` field (e.g. "success"), an optional `message`, and a `data`
payload. `PagedResponse` extends this with pagination metadata.
"""

from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status: str = Field(..., description="Result status, usually 'success' or 'error'")
    message: Optional[str] = Field(None, description="Human‑readable message")
    data: Optional[T] = Field(None, description="Payload data")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed",
                "data": None,
            }
        }

class PaginationMeta(BaseModel):
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number (1‑based)")
    size: int = Field(..., description="Page size (items per page)")
    pages: int = Field(..., description="Total pages")

class PagedResponse(BaseModel, Generic[T]):
    status: str = Field(..., description="Result status")
    message: Optional[str] = Field(None, description="Optional message")
    data: List[T] = Field(..., description="List of items for the current page")
    meta: PaginationMeta = Field(..., description="Pagination metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Fetched page 1",
                "data": [],
                "meta": {
                    "total": 0,
                    "page": 1,
                    "size": 20,
                    "pages": 0,
                },
            }
        }
