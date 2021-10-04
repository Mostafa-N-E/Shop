from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.OrderView.as_view(), name='order'),
    path('/order/create', views.CreateOrder.as_view(), name='order_create'),
]
