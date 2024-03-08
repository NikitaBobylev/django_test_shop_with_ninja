from abc import (
    ABC,
    abstractmethod,
)
from uuid import uuid4

from core.apps.customers.entities.customers import Customer as CustomerEntity
from core.apps.customers.models import Customer as CustomerModel


class BaseCustomerService(ABC):
    model = CustomerModel

    @abstractmethod
    def get_or_create(self, phone: str) -> CustomerEntity:
        ...

    @abstractmethod
    def get(self, phone: str) -> CustomerEntity:
        ...

    @abstractmethod
    def generate_token(self, customer: CustomerEntity) -> str:
        ...


class ORMCustomerService(BaseCustomerService):
    def get_or_create(self, phone: str) -> CustomerEntity:
        customer, _ = self.model.objects.get_or_create(
            phone=phone,
        )
        return customer.to_entity()

    def get(self, phone: str) -> CustomerEntity:
        customer = self.model.objects.get(
            phone=phone,
        )
        return customer.to_entity()

    def generate_token(self, customer: CustomerEntity) -> str:
        new_token = str(uuid4())
        self.model.objects.filter(
            phone=customer.phone,
        ).update(token=new_token)
        return new_token
