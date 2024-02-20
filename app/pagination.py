from .schemas import PageParams, PagedResponse, T, PageFilter
from pydantic import BaseModel
from .address.schemas import Address
from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import Query
from .database import Base
from typing import List, Optional


def filter(page_params: PageParams, query: Query, ResponseSchema: BaseModel, ResponseModel: Base, searchField: Optional[List[str]]) -> PagedResponse[T]:
    """Paginate and sort the query."""

    def sort(val: str, field: str):
        if (val == 'desc'):
            return desc(getattr(ResponseModel, field))
        else:
            return asc(getattr(ResponseModel, field))

    if page_params.q and searchField:
        arr = [getattr(ResponseModel, field).ilike(page_params.q + '%')
               for field in searchField]
        query = query.filter(or_(*arr))

    if (page_params.sort):
        query = query.order_by(sort(page_params.sort, page_params.sort_field))

    paginated_query = query.offset(
        (page_params.page - 1) * page_params.size).limit(page_params.size)

    return PagedResponse(
        page_filter=PageFilter(total=query.count(), page=page_params.page,
                               size=page_params.size,
                               sort=page_params.sort,
                               sort_field=page_params.sort_field,
                               q=page_params.q),

        results=[ResponseSchema.model_validate(
            item) for item in paginated_query.all()]
    )
