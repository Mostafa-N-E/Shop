from django.contrib import admin
from .models import Order, OrderItem, BaseOrder

# Register models.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']

@admin.register(BaseOrder)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','created', 'updated', 'paid'] # , 'customer'
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]