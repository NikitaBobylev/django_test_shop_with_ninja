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
from core.apps.customers.services.auth import AuthCustomerService
from core.apps.customers.services.codes import DjangoCacheCodeService
from core.apps.customers.services.customer import ORMCustomerService
from core.apps.customers.services.sender import TerminalSenderService


router = Router(tags=['Customers'])


@router.post('create-customer', response=ApiResponse[LogOutSchema])
def create_customer(request: HttpRequest, customer_info: LogInSchema):
    service = AuthCustomerService(
        code_service=DjangoCacheCodeService(),
        customer_service=ORMCustomerService(),
        sender_service=TerminalSenderService(),
    )
    service.authorize(phone=customer_info.phone)
    message = f'send code on customer - {customer_info.phone}'
    return ApiResponse(
        data=LogOutSchema(
            message=message,
        ),
    )


@router.post('confirm_code', response=ApiResponse[ConfirmOutSchema])
def confirm_code(request: HttpRequest, confirm_information: ConfirmInSchema) -> ApiResponse:
    service = AuthCustomerService(
        code_service=DjangoCacheCodeService(),
        customer_service=ORMCustomerService(),
        sender_service=TerminalSenderService(),
    )
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
