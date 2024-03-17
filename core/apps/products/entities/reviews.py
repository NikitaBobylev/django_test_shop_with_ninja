from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from core.apps.common.enums import EntityStatus
from core.apps.customers.entities.customers import Customer
from core.apps.products.entities.products import Product


@dataclass
class Review:
    id: int | None = field(default=None, kw_only=True)  # noqa

    product: Product | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    customer: Customer | EntityStatus = field(default=EntityStatus.NOT_LOADED)

    text: str | None = field(default='')
    rating: int | None = field(default=1)

    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)
