from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class ReviewAlreadyExistException(ServiceException):
    product_id: int
    customer_id: int

    @property
    def message(self):
        return (
            f'Review for product - {self.product_id} from \\'
            f'customer {self.customer_id} already exist'
        )


@dataclass(eq=False)
class RatingNotValidException(ServiceException):
    rating: int

    @property
    def message(self) -> str:
        return f'rating - {self.rating} is not valid'
