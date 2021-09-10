from django.contrib import admin
from .models import Order, OrderItem

# Register models.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer','created', 'updated', 'paid']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]