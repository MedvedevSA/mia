from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import OrderDetailRepository
from schemas.order_detail import (
    AddOrderDetail,
    UpdOrderDetail,
    OrderDetailSchema
)
from services import BaseService
from utils.utils import module_url

r = APIRouter()
BASE = module_url(__name__)


def service_depends():
    return BaseService(OrderDetailRepository)


ServiceDepends = Annotated[BaseService, Depends(service_depends)]


@r.post(BASE)
async def add_order_detail(
    order_detail: AddOrderDetail,
    order_detail_srvc: ServiceDepends
) -> int | None:
    return await order_detail_srvc.add_one(order_detail)


@r.get(BASE)
async def get_order_details(
    order_detail_srvc: ServiceDepends
) -> list[OrderDetailSchema]:
    return await order_detail_srvc.get_all(response_model=OrderDetailSchema)


@r.get(BASE + '/{id}')
async def get_order_detail(
    id: int,
    order_detail_srvc: ServiceDepends
) -> OrderDetailSchema | None:
    return await order_detail_srvc.get_one(id, response_model=OrderDetailSchema)


@r.put(BASE + '/{id}')
async def update_order_detail(
    id: int,
    upd_order_detail: UpdOrderDetail,
    order_detail_srvc: ServiceDepends
) -> int | None:
    return await order_detail_srvc.update_one(id, upd_order_detail)


@r.delete(BASE + '/{id}')
async def delete_order_detail(
    id: int,
    order_detail_srvc: ServiceDepends
) -> int:
    return await order_detail_srvc.del_one(id)
