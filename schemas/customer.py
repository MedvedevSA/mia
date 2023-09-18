from pydantic import BaseModel


class AddCustomer(BaseModel):
    name: str
    phone: int
    comment: str


class UpdateCustomer(AddCustomer):
    ...


class BaseCustomer(UpdateCustomer):
    id: int
