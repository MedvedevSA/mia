from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from api.customers import get_customers, ServiceDepends, BASE
from schemas.customer import BaseCustomer, AddCustomer
from utils.qs import converted_qs

r = APIRouter()

templates = Jinja2Templates(directory='templates')


@r.get(BASE + '/create')
def get_customer_form(
    request: Request,
    context: str | None = None,
):
    return templates.TemplateResponse(
        'components/customers/create.html',
        context=dict(request=request, context=context)
    )


@r.get(BASE)
def customers_page(
    request: Request,
    customers: Annotated[list[BaseCustomer], Depends(get_customers)],
):
    return templates.TemplateResponse(
        'pages/customers.html',
        context=dict(request=request, customers=customers)
    )


@r.get(BASE + '/select_form')
async def get_select_form(
    request: Request,
):
    html = 'components/customers/select_form.html'
    return templates.TemplateResponse(
        html,
        context=dict(
            request=request,
        )
    )


@r.post(BASE)
async def add_customer(
    request: Request,
    body: Annotated[dict, Depends(converted_qs)],
    customer_srvc: ServiceDepends,
):
    context: str = body.get('context')
    html = 'components/customers/create.html'
    if context == 'select_form':
        html = 'components/customers/select_form.html'

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
