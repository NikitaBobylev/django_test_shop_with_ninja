from abc import (
    ABC,
    abstractmethod,
)

from core.apps.customers.entities.customers import Customer as CustomerEntity
from core.apps.customers.models import Customer as CustomerModel


class BaseCustomerService(ABC):
    model = CustomerModel

    @abstractmethod
    def get_or_create(self, phone: str) -> CustomerEntity:
        ...

    @abstractmethod
    def generate_token(self, customer: CustomerEntity) -> str:
        ...
