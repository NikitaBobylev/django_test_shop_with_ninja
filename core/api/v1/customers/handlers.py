from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
)
from ninja import Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.customers.schemas import (
    ConfirmInSchema,
    ConfirmOutSchema,
    LogInSchema,
    LogOutSchema,
)
from core.apps.common.exceptions import ServiceException
from core.apps.customers.services.auth import BaseAuthCustomerService
from core.project.containers import get_containers


router = Router(tags=['Customers'])


@router.post('create-customer', response=ApiResponse[LogOutSchema])
def create_customer(request: HttpRequest, customer_info: LogInSchema):
    service: BaseAuthCustomerService = get_containers().resolve(BaseAuthCustomerService)
    service.authorize(phone=customer_info.phone)
    message = f'send code on customer - {customer_info.phone}'
    return ApiResponse(
        data=LogOutSchema(
            message=message,
        ),
    )


@router.post('confirm_code', response=ApiResponse[ConfirmOutSchema])
def confirm_code(request: HttpRequest, confirm_information: ConfirmInSchema) -> ApiResponse:
    service: BaseAuthCustomerService = get_containers().resolve(BaseAuthCustomerService)
    try:
        token = service.confirm(
            code=confirm_information.code,
            phone=confirm_information.phone,
        )
    except ServiceException as exception:
        raise HttpError(
            status_code=HttpResponseBadRequest.status_code,
            message=exception.message,
        )

    return ApiResponse(
        data=ConfirmOutSchema(
            token=token,
            phone=confirm_information.phone,
        ),
    )
