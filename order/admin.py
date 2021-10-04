from django.contrib import admin
from .models import Order, OrderItem, BaseOrder

# Register models.

class OrderInline(admin.TabularInline):
    model = Order
    raw_id_field = ['order_items']

@admin.register(BaseOrder)
class BaseOrderAdmin(admin.ModelAdmin):
    list_display = ['id','created', 'updated', 'paid'] # , 'customer'
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','order_base',  'paymentـtrackingـcode']