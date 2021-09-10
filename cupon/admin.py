from django.contrib import admin
from .models import Cupon

# Register models.

@admin.register(Class)
class CuponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount']
    list_filter  = ['valid_from', 'valid_to']
    search_field = ['code']