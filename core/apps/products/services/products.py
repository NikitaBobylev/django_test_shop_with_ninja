from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import (
    Q,
    QuerySet,
)

from core.api.filters import PaginationIn
from core.apps.products.entities.products import (
    Product as ProductEntity,
    ProductFilter,
)
from core.apps.products.exceptions.products import ProductNotFoundException
from core.apps.products.models.products import Product as ProductModel


class BaseProductService(ABC):
    @abstractmethod
    def get_product_list(
            self,
            search: ProductFilter = ProductFilter(),
            pagination: PaginationIn = PaginationIn(),
    ) -> Iterable[ProductEntity]:
        ...

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> ProductEntity:
        ...

    @abstractmethod
    def get_product_count(self, search: ProductFilter = ProductFilter()) -> int:
        ...


class ORMProductService(BaseProductService):
    def __init__(self):
        self.model = ProductModel

    @staticmethod
    def _build_query(search: ProductFilter) -> Q:
        qs = Q(is_visible=True)
        if search.search is not None:
            qs &= Q(title__icontains=search.search) | Q(
                description__icontains=search.search,
            )
        return qs

    def get_product_list(
            self,
            search: ProductFilter = ProductFilter(),
            pagination: PaginationIn = PaginationIn(),
    ) -> Iterable[ProductEntity]:
        qs: QuerySet = self.model.objects.filter(
            self._build_query(search),
        )[pagination.offset: pagination.offset + pagination.limit]
        return [product.to_entity() for product in qs]

    def get_product_count(self, search: ProductFilter = ProductFilter()) -> int:
        query = self._build_query(search)
        return self.model.objects.filter(query).count()

    def get_product_by_id(self, product_id: int) -> ProductEntity:
        try:
            product = self.model.objects.get(id=product_id)
        except self.model.DoesNotExist:
            raise ProductNotFoundException(
                product_id=product_id,
            )
        return product.to_entity()
