from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
)
from ninja import (
    Header,
    Router,
)
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.reviews.schemas import (
    ReviewInSchema,
    ReviewOutSchema,
    ReviewUpdateInSchema,
)
from core.apps.common.exceptions import ServiceException
from core.apps.products.entities.reviews import Review as ReviewEntity
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase
from core.apps.products.use_cases.reviews.delete import DeleteReviewUseCase
from core.apps.products.use_cases.reviews.update import UpdateReviewUseCase
from core.project.containers import get_containers


router = Router(tags=['Reviews'])
container = get_containers()


@router.post('{product_id}/review', response=ApiResponse[ReviewOutSchema])
def create_review(
        request: HttpRequest,
        token: Header[str],
        product_id: int,
        review: ReviewInSchema,
) -> ApiResponse[ReviewOutSchema]:
    use_case: CreateReviewUseCase = container.resolve(CreateReviewUseCase)
    try:
        review = use_case.execute(
            token=token,
            product_id=product_id,
            review=review.to_entity(),
        )
    except ServiceException as ex:
        raise HttpError(
            status_code=HttpResponseBadRequest.status_code,
            message=ex.message,
        )
    return ApiResponse(
        data=ReviewOutSchema.from_entity(review),
    )


@router.put('{product_id}/review', response=ApiResponse[ReviewOutSchema])
def update_review(
        request: HttpRequest,
        token: Header[str],
        product_id: int,
        review: ReviewUpdateInSchema,
) -> ApiResponse[ReviewOutSchema]:
    use_case: UpdateReviewUseCase = container.resolve(UpdateReviewUseCase)
    try:
        review = use_case.execute(
            token=token,
            product_id=product_id,
            review=review.to_entity(),
        )
    except ServiceException as ex:
        raise HttpError(
            status_code=HttpResponseBadRequest.status_code,
            message=ex.message,
        )
    return ApiResponse(
        data=ReviewOutSchema.from_entity(review),
    )


@router.delete('{product_id}/review', response=ApiResponse[ReviewOutSchema])
def delete_review(
        request: HttpRequest,
        token: Header[str],
        product_id: int,
) -> ApiResponse[ReviewOutSchema]:
    use_case: DeleteReviewUseCase = container.resolve(DeleteReviewUseCase)
    try:
        review = use_case.execute(
            token=token,
            product_id=product_id,
            review=ReviewEntity(),
        )
    except ServiceException as ex:
        raise HttpError(
            status_code=HttpResponseBadRequest.status_code,
            message=ex.message,
        )
    return ApiResponse(
        data=ReviewOutSchema.from_entity(review),
    )
