from typing import Annotated
from datetime import datetime, date

from pydantic import BaseModel, Field, BeforeValidator, ValidationError

from utils.paging import PagingModel


def convert_to_date(v: str) -> date:
    v = v.split("/")
    if len(v) == 3:
        d, m, y = map(int, v)
        return date(y, m, d)
    else:
        raise ValidationError('Не верный формат даты YYYY/MM/DD')


class AddOrder(BaseModel):
    customer_id: int = Field(ge=1)
    due_date: Annotated[date, BeforeValidator(convert_to_date)]
    comment: str = ''


class UpdOrder(AddOrder):
    completion_date: datetime | None
    passed: bool
    ...


class BaseOrder(UpdOrder):
    id: int
    time_created: datetime


class OrderFilter(PagingModel):
    customer_id: int
