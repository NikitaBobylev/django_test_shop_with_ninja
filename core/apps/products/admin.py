from django.contrib import admin
from core.apps.products.models.products import Product


@admin.register(Product)
class ProductAdminModel(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'updated_at', 'is_visible')

