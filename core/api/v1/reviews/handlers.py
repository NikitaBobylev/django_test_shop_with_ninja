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
)
from core.apps.common.exceptions import ServiceException
from core.apps.products.use_cases.reivews import CreateReviewUseCase
from core.project.containers import get_containers


router = Router(tags=['Reviews'])


@router.post('{product_id}/review', response=ApiResponse[ReviewOutSchema])
def create_review(
        request: HttpRequest,
        token: Header[str],
        product_id: int,
        review: ReviewInSchema,
) -> ApiResponse[ReviewOutSchema]:
    container = get_containers()
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
