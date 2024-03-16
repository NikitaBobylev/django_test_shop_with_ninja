from typing import Iterable

from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)

from core.api.filters import (
    PaginationIn,
    PaginationOut,
)
from core.api.schemas import (
    ApiResponse,
    ListPaginationResponce,
)
from core.api.v1.products.filters import ProductFilter
from core.api.v1.products.schemas import ProductSchema
from core.apps.products.entities.products import ProductFilter as ProductFilterEntity
from core.apps.products.services.products import BaseProductService
from core.project.containers import get_containers


product_router = Router(tags=['Products'])


@product_router.get('', response=ApiResponse[ListPaginationResponce[ProductSchema]])
def get_product_list_handler(
        request: HttpRequest,
        search: Query[ProductFilter],
        pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginationResponce[ProductSchema]]:
    service: BaseProductService = get_containers().resolve(BaseProductService)
    product_list = service.get_product_list(
        search=ProductFilterEntity(search=search.search),
        pagination=pagination_in,
    )
    product_total: int = service.get_product_count(search=search)
    items: Iterable[ProductSchema] = [
        ProductSchema.from_entity(obj) for obj in product_list
    ]
    pagination: PaginationOut = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=product_total,
    )
    return ApiResponse(
        data=ListPaginationResponce(
            items=items,
            pagination=pagination,
        ),
    )
