from datetime import datetime

from ninja import Schema

from core.apps.products.entities.products import Product as ProductEntity


# TODO: create new common endpoint
class ProductSchema(Schema):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: ProductEntity) -> 'ProductSchema':
        return ProductSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


ProductListSchema = list[ProductSchema]
