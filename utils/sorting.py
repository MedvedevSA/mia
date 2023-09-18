from typing import Literal

from fastapi import Query
from pydantic import BaseModel

SortOrder = Literal['asc', 'desc']


class SortParam(BaseModel):
    sort_col: str | None = Query(default=None)


class SortOrderParam(SortParam):
    sort_order: SortOrder = Query(default='asc')

