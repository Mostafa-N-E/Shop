from django.contrib import admin
from .models import Customer

# Register models.

# --------------------------------------------------CUSTOMER----------------------------------------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', ]
    # list_editable = ['address','postal_code','city',]
    search_fields = ['phone_number', ]