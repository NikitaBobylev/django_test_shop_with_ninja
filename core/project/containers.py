from functools import lru_cache

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


@lru_cache(1)
def get_containers() -> punq.Container:
    return _init_containers()


def _init_containers() -> punq.Container:
    container: punq.Container = punq.Container()

    # product container
    container.register(BaseProductService, ORMProductService)

    # auth customer service
    container.register(BaseCodeService, DjangoCacheCodeService)
    container.register(BaseSendersService, TerminalSenderService)
    container.register(BaseCustomerService, ORMCustomerService)
    container.register(BaseAuthCustomerService, AuthCustomerService)
    return container
