from django.contrib import admin

from core.apps.customers.models import Customer


@admin.register(Customer)
class CustomerAdminModel(admin.ModelAdmin):
    list_display = (
        'id',
        'phone',
        'token',
        'created_at',
        'updated_at',
    )
