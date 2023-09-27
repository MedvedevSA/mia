from typing import Annotated
from fastapi import APIRouter, Request, Depends, Header, Body, Query
from fastapi.templating import Jinja2Templates

from api.customer import get_customers, service_depends, ServiceDepends
from schemas.customer import BaseCustomer, AddCustomer, CustomerFiler
from utils.qs import converted_qs

r = APIRouter()

templates = Jinja2Templates(directory='templates')


@r.get('/customer/new')
def get_customer_form(
    request: Request,
    context: str | None = None,
):
    return templates.TemplateResponse(
        'components/customer/new.html',
        context=dict(request=request, context=context)
    )


@r.get('/customer')
def customers_page(
    request: Request,
    customers: Annotated[list[BaseCustomer], Depends(get_customers)],
):
    return templates.TemplateResponse(
        'pages/customer.html',
        context=dict(request=request, customers=customers)
    )


@r.get('/customer/select_form')
async def get_select_form(
    request: Request,
):
    html = 'components/customer/select_form.html'
    return templates.TemplateResponse(
        html,
        context=dict(
            request=request,
        )
    )


@r.post('/customer')
async def add_customer(
    request: Request,
    body: Annotated[dict, Depends(converted_qs)],
    customer_srvc: ServiceDepends,
):
    context: str = body.get('context')
    html = 'components/customer/new.html'
    if context == 'select_form':
        html = 'components/customer/select_form.html'

    id = await customer_srvc.add_one(
        AddCustomer.model_validate(body)
    )
    customer = await customer_srvc.get_one(id, BaseCustomer)
    return templates.TemplateResponse(
        html,
        context=dict(
            request=request,
            context=context,
            customer=customer
        )
    )
