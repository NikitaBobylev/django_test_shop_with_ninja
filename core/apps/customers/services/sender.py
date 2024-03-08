from abc import (
    ABC,
    abstractmethod,
)

from core.apps.customers.entities.customers import Customer


class BaseSendersService(ABC):
    @abstractmethod
    def send_code(self, customer: Customer, code: str) -> None:
        ...


class TerminalSenderService(BaseSendersService):
    def send_code(self, customer: Customer, code: str) -> None:
        print(f'send to {customer.phone} code: {code}')
