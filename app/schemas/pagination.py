from pydantic import BaseModel, Field
from typing_extensions import Annotated
from typing import Generic, TypeVar, List
from enum import Enum
from typing import Optional


class PageParams(BaseModel):
    page: Annotated[int, Field(ge=1)] = 1
    size: Annotated[int, Field(ge=1, le=100)] = 10
    sort: Optional[str] = None
    sort_field: Optional[str] = None
    q: Optional[str] = None


T = TypeVar("T")


class PageFilter(BaseModel):
    total: int
    page: int
    size: int
    sort: Optional[str] = None
    sort_field: Optional[str] = None
    q: Optional[str] = None


class PagedResponse(BaseModel, Generic[T]):
    page_filter: PageFilter
    results: List[T]
