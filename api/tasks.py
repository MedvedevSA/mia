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
async def add_task(
    task: BaseTask,
    task_srvc: ServiceDepends
) -> int | None:
    return await task_srvc.add_one(task)


@r.get(BASE)
async def get_tasks(
    task_srvc: ServiceDepends
) -> list[TaskSchema]:
    return await task_srvc.get_all(response_model=TaskSchema)


@r.get(BASE + '/{id}')
async def get_task(
    id: int,
    task_srvc: ServiceDepends
) -> TaskSchema | None:
    return await task_srvc.get_one(id, response_model=TaskSchema)


@r.put(BASE + '/{id}')
async def update_task(
    id: int,
    upd_task: UpdTask,
    task_srvc: ServiceDepends
) -> int | None:
    return await task_srvc.update_one(id, upd_task)


@r.delete(BASE + '/{id}')
async def delete_task(
    id: int,
    task_srvc: ServiceDepends
) -> int:
    return await task_srvc.del_one(id)
