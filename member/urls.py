from django.urls import path, include
from . import views
urlpatterns = [
    path('login/',views.LoginView.as_view(), name='customer_login' ),
    path('registration/',views.RegisterView.as_view(), name='customer_register' ),

]
