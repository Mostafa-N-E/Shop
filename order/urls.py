from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.OrderView.as_view(), name='order'),
    path('/create/', views.CreateOrder.as_view(), name='order_create'),
    path('/orders-list/', views.ListOrder.as_view(), name='list_orders'),
    path('orders-detail/<int:pk>', views.DetailOrder.as_view(), name='detail_order'),
]
