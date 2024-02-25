from ninja import Schema
from datetime import datetime


class ProductSchema(Schema):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime


ProductListSchema = list[ProductSchema]
