from urllib.parse import parse_qs

from typing import Annotated
from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates

from api.order import ServiceDepends
from schemas.order import AddOrder
from utils.qs import converted_qs

r = APIRouter()

templates = Jinja2Templates(directory='templates')


@r.get('/order/new')
def new_order_page(request: Request):
    return templates.TemplateResponse(
        'pages/order/new.html',
        context=dict(request=request)
    )


@r.get('/order')
def orders_page(request: Request):
    return templates.TemplateResponse(
        'pages/order/index.html',
        context=dict(request=request)
    )


@r.post('/order')
async def post_order(
    order_srvc: ServiceDepends,
    body: Annotated[dict, Depends(converted_qs)],
):
    new_order_id = await order_srvc.add_one(AddOrder.model_validate(body))
    return Response(headers={'HX-Redirect': f'/order/edit/{new_order_id}'})
