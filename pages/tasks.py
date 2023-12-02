from math import ceil
from urllib.parse import parse_qs

from typing import Annotated
from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates

from api.tasks import ServiceDepends
from schemas.task import BaseTask, TasksTable, TaskFilter
from utils.qs import converted_qs

r = APIRouter()

templates = Jinja2Templates(directory='templates')


@r.get('/tasks/create')
def new_task_page(request: Request):
    return templates.TemplateResponse(
        'forms/tasks/create.html',
        context=dict(request=request)
    )


@r.get('/tasks')
async def tasks_page(
    task_srvc: ServiceDepends,
    request: Request,
    filter: Annotated[TaskFilter, Depends()],
):
    tasks = await task_srvc.get_all(params=filter, response_model=TasksTable)
    pages_count = ceil(await task_srvc.repository.get_task_count() / filter.page_limit)
    return templates.TemplateResponse(
        'pages/tasks/index.html',
        context=dict(
            request=request,
            tasks=[row.model_dump() for row in tasks],
            filter=filter,
            pages_count=pages_count,
        )
    )


@r.post('/tasks')
async def post_task(
    task_srvc: ServiceDepends,
    body: Annotated[dict, Depends(converted_qs)],
):
    new_task_id = await task_srvc.add_one(BaseTask.model_validate(body))
    return Response(headers={'HX-Redirect': f'/tasks/edit/{new_task_id}'})
