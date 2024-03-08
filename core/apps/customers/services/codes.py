from abc import (
    ABC,
    abstractmethod,
)
from random import randrange  # noqa

from django.core.cache import cache

from core.apps.customers.entities.customers import Customer as CustomerEntity
from core.apps.customers.exceptions import (
    CodeNotEqualException,
    CodeNotFoundException,
)


class BaseCodeService(ABC):
    @abstractmethod
    def generate_code(self, customer: CustomerEntity) -> str:
        ...

    @abstractmethod
    def validate_code(self, code: str, customer: CustomerEntity) -> None:
        ...


class DjangoCacheCodeService(BaseCodeService):

    def generate_code(self, customer: CustomerEntity) -> str:
        code = str(randrange(100_000, 1_000_000))
        cache.set(customer.phone, code)
        return code

    def validate_code(self, code: str, customer: CustomerEntity) -> None:
        cache_code = cache.get(customer.phone)
        if cache_code is None:
            raise CodeNotFoundException(code=code)

        if cache_code != code:
            raise CodeNotEqualException(
                code=code,
                cached_code=cache_code,
                customer_phone=customer.phone,
            )
        cache.delete(customer.phone)
