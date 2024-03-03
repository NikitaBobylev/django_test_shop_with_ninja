from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.customers.services.codes import BaseCodeService
from core.apps.customers.services.customer import BaseCustomerService
from core.apps.customers.services.sender import BaseSendersService


@dataclass(eq=False)
class BaseAuthCustomerService(ABC):
    customer_service: BaseCustomerService
    code_service: BaseCodeService
    sender_service: BaseSendersService

    @abstractmethod
    def authorize(self, phone: str) -> None:
        ...

    @abstractmethod
    def confirm(self, token: str) -> None:
        ...


class AuthCustomerService(BaseAuthCustomerService):
    def authorize(self, phone: str) -> None:
        customer = self.customer_service.get_or_create(phone=phone)
        code = self.code_service.generate_code(customer=customer)
        self.sender_service.send_code(code)

    def confirm(self, token: str) -> None:
        ...
