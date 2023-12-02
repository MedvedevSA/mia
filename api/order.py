from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import TaskRepository
from schemas.task import BaseTask, UpdTask, TaskSchema
from services import BaseService
from utils.utils import module_url

r = APIRouter()
BASE = module_url(__name__)


def service_depends():
    return BaseService(TaskRepository)


ServiceDepends = Annotated[BaseService, Depends(service_depends)]


@r.post(BASE)
async def add_order(
    order: BaseTask,
    order_srvc: ServiceDepends
) -> int | None:
    return await order_srvc.add_one(order)


@r.get(BASE)
async def get_orders(
    order_srvc: ServiceDepends
) -> list[TaskSchema]:
    return await order_srvc.get_all(response_model=TaskSchema)


@r.get(BASE + '/{id}')
async def get_order(
    id: int,
    order_srvc: ServiceDepends
) -> TaskSchema | None:
    return await order_srvc.get_one(id, response_model=TaskSchema)


@r.put(BASE + '/{id}')
async def update_order(
    id: int,
    upd_order: UpdTask,
    order_srvc: ServiceDepends
) -> int | None:
    return await order_srvc.update_one(id, upd_order)


@r.delete(BASE + '/{id}')
async def delete_order(
    id: int,
    order_srvc: ServiceDepends
) -> int:
    return await order_srvc.del_one(id)
