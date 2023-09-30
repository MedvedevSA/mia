from datetime import datetime
from pydantic import BaseModel, Field


class BaseOrderDetail(BaseModel):
    description: str = ''
    cost: int = Field(ge=0)


class AddOrderDetail(BaseOrderDetail):
    order_id: int = Field(ge=1)


class UpdOrderDetail(AddOrderDetail):
    completion_date: datetime


class OrderDetailSchema(UpdOrderDetail):
    id: int
    time_created: datetime
