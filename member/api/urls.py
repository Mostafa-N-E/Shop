from django.urls import path, re_path
# from django.views.generic import TemplateView
#
# from .views import RegisterationView
#
# # app_name = 'member_api'
#
# urlpatterns = [
#     path('', RegisterationView.as_view(), name='rest_register'),
#
# ]


from django.urls import path, include

from .views import Register, RequestResetPasswordEmail

urlpatterns = [
    path('registration/', Register.as_view(), name='register'),
    path('password/reset/', RequestResetPasswordEmail.as_view(), name='password_reset'),
]
