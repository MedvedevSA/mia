from fastapi import Query
from pydantic import BaseModel


class PagingModel(BaseModel):
    page_number: int = Query(default=1)
    page_limit: int = Query(default=5, ge=1, le=1000)
