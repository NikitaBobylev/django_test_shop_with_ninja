from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.products.entities.reviews import Review as ReviewEntity


class Review(TimedBaseModel):
    product = models.ForeignKey(
        to='products.Product',
        related_name='product_review',
        verbose_name='Продукт',
        on_delete=models.CASCADE,

    )
    customer = models.ForeignKey(
        to='customers.Customer',
        related_name='customer_review',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,

    )
    rating = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Рейтинг',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        blank=True,
        default='',
    )

    @classmethod
    def from_entity(cls, review: ReviewEntity) -> 'Review':
        return cls(
            customer_id=review.customer.id,
            product_id=review.product.id,
            text=review.text,
            rating=review.rating,
        )

    def to_entity(self) -> ReviewEntity:
        return ReviewEntity(
            id=self.id,
            text=self.text,
            rating=self.rating,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('product', 'customer')
