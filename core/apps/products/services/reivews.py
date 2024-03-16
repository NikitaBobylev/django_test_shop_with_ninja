from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Iterable,
    NoReturn,
)

from core.apps.customers.entities.customers import Customer as CustomerEntity
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.entities.reviews import Review as ReviewEntity
from core.apps.products.exceptions.reivews import (
    RatingNotValidException,
    ReviewAlreadyExistException,
)
from core.apps.products.models import Review


class BaseReviewService(ABC):
    model = Review

    @abstractmethod
    def is_review_exists(
            self,
            product: ProductEntity,
            customer: CustomerEntity,
    ) -> bool:
        ...

    @abstractmethod
    def create_review(
            self,
            review: ReviewEntity,
    ) -> ReviewEntity:
        ...


class OrmReviewService(BaseReviewService):
    def is_review_exists(
            self,
            product: ProductEntity,
            customer: CustomerEntity,
    ) -> bool:
        return self.model.objects.filter(
            product_id=product.id, customer_id=customer.id,
        ).exists()

    def create_review(
            self,
            review: ReviewEntity,
    ) -> ReviewEntity:
        review_dto = self.model.from_entity(
            review,
        )
        review_dto.save()
        return review_dto.to_entity()


class BaseReviewValidator(ABC):
    @abstractmethod
    def validate(self, review: ReviewEntity) -> NoReturn | None:
        ...


class ReviewRatingValidator(BaseReviewValidator):
    def validate(self, review: ReviewEntity) -> NoReturn | None:
        if not 1 <= review.rating <= 5:
            raise RatingNotValidException(rating=review.rating)


@dataclass
class SingleReviewValidator(BaseReviewValidator):
    review_service: BaseReviewService

    def validate(self, review: ReviewEntity) -> NoReturn | None:
        if self.review_service.is_review_exists(
                customer=review.customer,
                product=review.product,
        ):
            raise ReviewAlreadyExistException(
                product_id=review.product.id,
                customer_id=review.customer.id,
            )


@dataclass
class ComposedReviewValidator(BaseReviewValidator):
    validators: Iterable[BaseReviewValidator]

    def validate(self, review: ReviewEntity) -> NoReturn | None:
        for validator in self.validators:
            validator.validate(review)
