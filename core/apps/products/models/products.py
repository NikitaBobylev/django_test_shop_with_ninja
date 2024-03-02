from django.db import models

from core.apps.products.entities.products import Product as ProductEntity

from ...common.models import TimedBaseModel


class Product(TimedBaseModel):
    title = models.CharField(
        max_length=250,
        verbose_name='Название товара',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание товара',
    )
    is_visible = models.BooleanField(
        verbose_name='Виден ли товар в каталоге',
        default=True,
    )

    def to_entity(self) -> ProductEntity:
        return ProductEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
