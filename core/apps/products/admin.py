from django.contrib import admin

from core.apps.products.models import Review
from core.apps.products.models.products import Product


@admin.register(Product)
class ProductAdminModel(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'created_at',
        'updated_at',
        'is_visible',
    )


@admin.register(Review)
class ProductRatingModel(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'product',
        'text',
        'rating',
        'created_at',
        'updated_at',
    )
    list_select_related = ('customer', 'product')
