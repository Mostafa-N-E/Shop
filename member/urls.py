from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='customer_login'),
    path('registration/', views.RegisterView.as_view(), name='customer_register'),
    path('profile/', views.ProfileView.as_view(), name='customer_profile'),
    path('profile/edit-info/', views.Profile_edit.as_view(), name='customer_profile_edit'),
    path('password/change/', views.PasswordChangeView.as_view(), name='customer_password_change'),
    path('password/reset/', views.PasswordResetView.as_view(), name='customer_password_reset'),

]
