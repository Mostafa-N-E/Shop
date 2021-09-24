from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('home/', views.Products.as_view(), name='show_products'),
    path('category-products/<slug>', views.Category_Products.as_view(), name='show_category_products'),
    path('product_detail/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('change_lang/', views.change_lang, name='change_lang'),
]
