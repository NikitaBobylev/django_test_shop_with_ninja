from dataclasses import dataclass

from core.apps.customers.services.customer import BaseCustomerService
from core.apps.products.entities.reviews import Review as ReviewEntity
from core.apps.products.services.products import BaseProductService
from core.apps.products.services.reivews import (
    BaseReviewCreateValidator,
    BaseReviewService,
)


@dataclass(eq=False)
class CreateReviewUseCase:
    customer_service: BaseCustomerService
    product_service: BaseProductService
    review_service: BaseReviewService
    validator_service: BaseReviewCreateValidator

    def execute(
            self,
            token: str,
            product_id: int,
            review: ReviewEntity,

    ) -> ReviewEntity:
        customer = self.customer_service.get_customer_by_token(
            token=token,
        )
        product = self.product_service.get_product_by_id(
            product_id=product_id,
        )

        review.customer = customer
        review.product = product

        self.validator_service.validate(review)
        result_review: ReviewEntity = self.review_service.create_review(
            review,
        )
        return result_review
