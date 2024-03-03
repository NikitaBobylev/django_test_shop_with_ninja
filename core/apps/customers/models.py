from uuid import uuid4

from django.db import models

from core.apps.common.models import TimedBaseModel


class Customer(TimedBaseModel):
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        unique=True,
    )
    token = models.CharField(
        max_length=255,
        verbose_name='Токен',
        unique=True,
        default=uuid4,
    )

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
