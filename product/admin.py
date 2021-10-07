from gettext import ngettext

from django.contrib import admin, messages

# Register models.

from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name_en', )}
    # list_editable = ['image']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'category', 'name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available',]
    prepopulated_fields = {'slug': ('name_en', )}

    @admin.action(description="تغییر وضعیت محصول به  'در دسترس'")
    def change_availableــtrue(self, request, queryset):
        update = queryset.update(available=True)
        self.message_user(request, ngettext(
            '  %d مورد با موفقیت تغییر یافت', '  %d مورد با موفقیت تغییر یافتند',
            update, ) % update, messages.SUCCESS)

    @admin.action(description="تغییر وضعیت محصول به  'خارج دسترس'")
    def change_availableــfalse(self, request, queryset):
        update = queryset.update(available=False)
        self.message_user(request, ngettext(
            '  %d مورد با موفقیت تغییر یافت', '  %d مورد با موفقیت تغییر یافتند',
            update, ) % update, messages.SUCCESS)

    actions = [change_availableــtrue, change_availableــfalse, ]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'updated']
    list_editable = ['image']



