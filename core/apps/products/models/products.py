from django.db import models

from ...common.models import TimedBaseModel


class Product(TimedBaseModel):
    title = models.CharField(
        max_length=250,
        verbose_name='Название товара'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание товара',
    )
    is_visible = models.BooleanField(
        verbose_name='Виден ли товар в каталоге',
        default=True,

    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
