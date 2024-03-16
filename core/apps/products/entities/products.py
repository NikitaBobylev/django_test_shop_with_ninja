from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime


@dataclass
class Product:
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime

    def __str__(self):
        return self.title


@dataclass
class ProductFilter:
    search: str | None = field(default=None)
