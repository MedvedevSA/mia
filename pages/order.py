from urllib.parse import parse_qs

from typing import Annotated
from fastapi import APIRouter, Request, Depends, Header, Body
from fastapi.templating import Jinja2Templates

from schemas.customer import BaseCustomer, AddCustomer
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
