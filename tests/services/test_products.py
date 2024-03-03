import pytest

from core.apps.products.services.products import BaseProductService

from ..factories import ProductModelFactory


@pytest.mark.django_db
def test_products_count_zero(product_service: BaseProductService):
    products_count = product_service.get_product_count()
    assert isinstance(products_count, int), products_count
    assert products_count == 0, f'{products_count=} is not zero'


@pytest.mark.django_db
def test_products_count_not_zero(product_service: BaseProductService):
    size = 5
    ProductModelFactory.create_batch(size=size)
    products_count = product_service.get_product_count()
    assert isinstance(products_count, int), products_count
    assert products_count == size, f'{products_count=} is not zero'


@pytest.mark.django_db
def test_products_list_zero(product_service: BaseProductService):
    products_list = product_service.get_product_list()
    assert products_list == [], f'{products_list=} is not empty'


@pytest.mark.django_db
def test_products_list_exist(product_service: BaseProductService):
    expected_size = 5
    factory_products = [
        i.id for i in
        ProductModelFactory.create_batch(size=expected_size)
    ]
    products_list = [i.id for i in product_service.get_product_list()]
    assert sorted(factory_products) == sorted(products_list)
