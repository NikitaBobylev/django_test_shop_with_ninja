from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class ProductNotFoundException(ServiceException):
    product_id: int

    @property
    def message(self):
        return f'Product not found Product - {self.product_id}'
