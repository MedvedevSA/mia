from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import OrderRepository
from schemas.order import AddOrder, UpdOrder, BaseOrder
from services import BaseService
from utils.utils import module_url

r = APIRouter()
BASE = module_url(__name__)


def service_depends():
    return BaseService(OrderRepository)


ServiceDepends = Annotated[BaseService, Depends(service_depends)]


@r.post(BASE)
async def add_order(
    order: AddOrder,
    order_srvc: ServiceDepends
) -> int | None:
    return await order_srvc.add_one(order)


@r.get(BASE)
async def get_orders(
    order_srvc: ServiceDepends
) -> list[BaseOrder]:
    return await order_srvc.get_all(response_model=BaseOrder)


@r.get(BASE + '/{id}')
async def get_order(
    id: int,
    order_srvc: ServiceDepends
) -> BaseOrder | None:
    return await order_srvc.get_one(id, response_model=BaseOrder)


@r.put(BASE + '/{id}')
async def update_order(
    id: int,
    upd_order: UpdOrder,
    order_srvc: ServiceDepends
) -> int | None:
    return await order_srvc.update_one(id, upd_order)


@r.delete(BASE + '/{id}')
async def delete_order(
    id: int,
    order_srvc: ServiceDepends
) -> int:
    return await order_srvc.del_one(id)
