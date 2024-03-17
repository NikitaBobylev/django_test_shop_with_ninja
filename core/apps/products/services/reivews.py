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
    ReviewDoesNotExist,
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

    @abstractmethod
    def update_review(
            self,
            review: ReviewEntity,
    ) -> ReviewEntity:
        ...


class OrmReviewService(BaseReviewService):
    def _get_model_elem_by_customer_product(self, review: ReviewEntity) -> Review:
        return self.model.objects.get(
            customer_id=review.customer.id,
            product_id=review.product.id,
        )

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

    def update_review(
            self,
            review: ReviewEntity,
    ) -> ReviewEntity:
        review_dto = self._get_model_elem_by_customer_product(review=review)

        if review.text is not None:
            review_dto.text = review.text

        if review.rating is not None:
            review_dto.rating = review.rating

        review_dto.save()
        return review_dto.to_entity()


class BaseReviewValidator(ABC):
    @abstractmethod
    def validate(self, review: ReviewEntity) -> NoReturn | None:
        ...


class BaseReviewCreateValidator(BaseReviewValidator):
    @abstractmethod
    def validate(self, review: ReviewEntity) -> NoReturn | None:
        ...


class BaseReviewUpdateValidator(BaseReviewValidator):
    @abstractmethod
    def validate(self, review: ReviewEntity) -> NoReturn | None:
        ...


class ReviewRatingValidator(BaseReviewCreateValidator):
    def validate(self, review: ReviewEntity) -> NoReturn | None:
        if type(review.rating) is int and not 1 <= review.rating <= 5:
            raise RatingNotValidException(rating=review.rating)


@dataclass
class SingleReviewValidator(BaseReviewCreateValidator):
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
class SingleExistReviewValidator(BaseReviewUpdateValidator):
    validator_service: SingleReviewValidator

    def validate(self, review: ReviewEntity) -> NoReturn | None:
        try:
            self.validator_service.validate(review=review)
        except ReviewAlreadyExistException:
            pass
        else:
            raise ReviewDoesNotExist(
                product_id=review.product.id,
                customer_id=review.customer.id,
            )


@dataclass
class ComposedReviewValidator(BaseReviewCreateValidator, BaseReviewUpdateValidator):
    validators: Iterable[BaseReviewValidator]

    def validate(self, review: ReviewEntity) -> NoReturn | None:
        for validator in self.validators:
            validator.validate(review)
