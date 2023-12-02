from typing import Annotated
from datetime import datetime, date

from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_serializers import PlainSerializer


from utils.paging import PagingModel
from utils.sorting import SortOrderParam


def convert_to_date(v: str) -> date:
    if isinstance(v, str):
        v = v.split("/")
        if len(v) == 3:
            d, m, y = map(int, v)
            return date(y, m, d)
        else:
            raise ValidationError('Не верный формат даты YYYY/MM/DD')
    return v


def datetime_serializer(v: datetime) -> str:
    return v.strftime("%d.%m.%y %H:%M")


datetimeSerialized = Annotated[datetime, PlainSerializer(datetime_serializer)]


class BaseTask(BaseModel):
    customer_id: int = Field(ge=1)


class UpdTask(BaseTask):
    completion_date: datetime | None


class TaskSchema(UpdTask):
    id: int
    time_created: datetime


class TasksTable(TaskSchema):
    time_created: datetimeSerialized


class TaskFilter(PagingModel, SortOrderParam):
    # customer_id: int | None = Query()
    ... 
