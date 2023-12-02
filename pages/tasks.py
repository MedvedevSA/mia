from math import ceil
from urllib.parse import parse_qs

from typing import Annotated
from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates

from api.order import ServiceDepends
from schemas.task import BaseTask, TasksTable, TaskFilter
from utils.qs import converted_qs

r = APIRouter()

templates = Jinja2Templates(directory='templates')


@r.get('/tasks/create')
def new_order_page(request: Request):
    return templates.TemplateResponse(
        'forms/tasks/create.html',
        context=dict(request=request)
    )


@r.get('/tasks')
async def tasks_page(
    order_srvc: ServiceDepends,
    request: Request,
    filter: Annotated[TaskFilter, Depends()],
):
    orders = await order_srvc.get_all(params=filter, response_model=TasksTable)
    pages_count = ceil(await order_srvc.repository.get_order_count() / filter.page_limit)
    return templates.TemplateResponse(
        'pages/tasks/index.html',
        context=dict(
            request=request,
            orders=[row.model_dump() for row in orders],
            filter=filter,
            pages_count=pages_count,
        )
    )


@r.post('/order')
async def post_order(
    order_srvc: ServiceDepends,
    body: Annotated[dict, Depends(converted_qs)],
):
    new_order_id = await order_srvc.add_one(BaseTask.model_validate(body))
    return Response(headers={'HX-Redirect': f'/order/edit/{new_order_id}'})
