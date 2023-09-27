import re
from typing import Annotated
from pydantic import BaseModel, BeforeValidator, Field

from utils.paging import PagingModel


def convert_mask(v: str) -> str:
    ''' +7 (999) 999-99-99 to 9999999999'''
    v = "".join(
        re.split('[ +()-]', v)
    )
    return v


class AddCustomer(BaseModel):
    name: str
    phone: Annotated[str, BeforeValidator(convert_mask)]
    comment: str = ''


class UpdateCustomer(AddCustomer):
    ...


class BaseCustomer(UpdateCustomer):
    id: int


class CustomerFiler(PagingModel):
    phone__ilike: str | None = Field(default=None, alias='phone_ilike')
