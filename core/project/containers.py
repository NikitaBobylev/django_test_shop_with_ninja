from functools import lru_cache
from logging import (
    getLogger,
    Logger,
)

import punq

from core.apps.customers.services.auth import (
    AuthCustomerService,
    BaseAuthCustomerService,
)
from core.apps.customers.services.codes import (
    BaseCodeService,
    DjangoCacheCodeService,
)
from core.apps.customers.services.customer import (
    BaseCustomerService,
    ORMCustomerService,
)
from core.apps.customers.services.sender import (
    BaseSendersService,
    TerminalSenderService,
)
from core.apps.products.services.products import (
    BaseProductService,
    ORMProductService,
)
from core.apps.products.services.reivews import (
    BaseReviewCreateValidator,
    BaseReviewService,
    BaseReviewUpdateDeleteValidator,
    BaseReviewValidator,
    ComposedReviewValidator,
    OrmReviewService,
    ReviewRatingValidator,
    SingleExistReviewValidator,
    SingleReviewValidator,
)
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase
from core.apps.products.use_cases.reviews.delete import DeleteReviewUseCase
from core.apps.products.use_cases.reviews.update import UpdateReviewUseCase


@lru_cache(1)
def get_containers() -> punq.Container:
    return _init_containers()


def _init_containers() -> punq.Container:
    container: punq.Container = punq.Container()
    container.register(Logger, factory=getLogger, name='django.request')

    # product container
    container.register(BaseProductService, ORMProductService)

    # auth customer service
    container.register(BaseCodeService, DjangoCacheCodeService)
    container.register(BaseSendersService, TerminalSenderService)
    container.register(BaseCustomerService, ORMCustomerService)
    container.register(BaseAuthCustomerService, AuthCustomerService)

    # review service
    container.register(BaseReviewService, OrmReviewService)

    # review validators
    container.register(SingleReviewValidator)
    container.register(ReviewRatingValidator)
    container.register(SingleExistReviewValidator)

    def build_create_validators() -> BaseReviewValidator:
        return ComposedReviewValidator(
            validators=(
                container.resolve(SingleReviewValidator),
                container.resolve(ReviewRatingValidator),
            ),
        )

    def build_update_validators() -> BaseReviewValidator:
        return ComposedReviewValidator(
            validators=(
                container.resolve(SingleExistReviewValidator),
                container.resolve(ReviewRatingValidator),
            ),
        )

    container.register(BaseReviewCreateValidator, factory=build_create_validators)
    container.register(BaseReviewUpdateDeleteValidator, factory=build_update_validators)

    # create review use-case
    container.register(CreateReviewUseCase)

    # update review use-case
    container.register(UpdateReviewUseCase)

    # delete review use-case
    container.register(DeleteReviewUseCase)

    return container
