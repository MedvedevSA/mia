from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import CustomerRepository
from schemas.customer import AddCustomer, UpdateCustomer, BaseCustomer, CustomerFiler
from services import BaseService
from utils.utils import module_url

r = APIRouter()
BASE = module_url(__name__)


def service_depends():
    return BaseService(CustomerRepository)


ServiceDepends = Annotated[BaseService, Depends(service_depends)]


@r.post(BASE)
async def add_customer(
    customer: AddCustomer,
    customer_srvc: ServiceDepends
) -> int | None:
    return await customer_srvc.add_one(customer)


@r.get(BASE)
async def get_customers(
    filter: Annotated[CustomerFiler, Depends()],
    customer_srvc: ServiceDepends
) -> list[BaseCustomer]:
    return await customer_srvc.get_all(
        params=filter, response_model=BaseCustomer
    )


@r.get(BASE + '/{id}')
async def get_customer(
    id: int,
    customer_srvc: ServiceDepends
) -> BaseCustomer | None:
    return await customer_srvc.get_one(id, response_model=BaseCustomer)


@r.put(BASE + '/{id}')
async def update_customer(
    id: int,
    upd_customer: UpdateCustomer,
    customer_srvc: ServiceDepends
) -> int | None:
    return await customer_srvc.update_one(id, upd_customer)


@r.delete(BASE + '/{id}')
async def delete_customer(
    id: int,
    customer_srvc: ServiceDepends
) -> int:
    return await customer_srvc.del_one(id)
