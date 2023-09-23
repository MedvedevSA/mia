from typing import Annotated
from fastapi import APIRouter, Request, Depends, Header
from fastapi.templating import Jinja2Templates

from api.customer import get_customers, service_depends
from schemas.customer import BaseCustomer, AddCustomer
from utils.qs import converted_qs

r = APIRouter()

templates = Jinja2Templates(directory='templates')


@r.get('/customer/new')
def get_customer_form(
    request: Request,
    hx_request: Annotated[bool, Header()] = None,
):
    hx_request
    return templates.TemplateResponse(
        'pages/customer/new.html',
        context=dict(request=request)
    )


@r.get('/customer')
def customers_page(
    request: Request,
    customers: Annotated[list[BaseCustomer], Depends(get_customers)],
    hx_request: Annotated[bool, Header()] = None,
):
    hx_request
    return templates.TemplateResponse(
        'pages/customer.html',
        context=dict(request=request, customers=customers)
    )


@r.post('/customer')
async def add_customer(
    request: Request,
    body: Annotated[dict, Depends(converted_qs)],
    hx_request: Annotated[bool, Header()] = None,
):
    customer_srvc = service_depends()
    id = await customer_srvc.add_one(
        AddCustomer.model_validate(body)
    )

    return templates.TemplateResponse(
        'components/customer/new.html',
        context=dict(request=request)
    )
