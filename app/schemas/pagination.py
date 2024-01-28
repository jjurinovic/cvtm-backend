from pydantic import BaseModel, Field
from typing_extensions import Annotated
from typing import Generic, TypeVar, List


class PageParams(BaseModel):
    page: Annotated[int, Field(ge=1)] = 1
    size: Annotated[int, Field(ge=1, le=100)] = 10


T = TypeVar("T")


class PagedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    results: List[T]
