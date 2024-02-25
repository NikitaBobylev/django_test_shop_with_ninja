from ninja import Router
from django.http import HttpRequest
from core.api.v1.products.schemas import ProductListSchema
from core.apps.products.models import Product

product_router = Router(tags=['Products'])


@product_router.get("", response=ProductListSchema)
def get_product_list_handler(request: HttpRequest) -> ProductListSchema:
    return Product.objects.all()
