from abc import (
    ABC,
    abstractmethod,
)

from core.apps.customers.entities.customers import Customer as CustomerEntity


class BaseCodeService(ABC):
    @abstractmethod
    def generate_code(self, customer: CustomerEntity) -> str:
        ...

    @abstractmethod
    def validate_code(self, code: str, customer: CustomerEntity) -> None:
        ...
