from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('add/', views.basket_add, name='add_basket'),
    path('remove/', views.basket_remove, name='remove_basket'),
    path('items/', views.BasketView.as_view(), name='basket'),

]
