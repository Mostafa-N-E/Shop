from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = "member/login.html"


class RegisterView(TemplateView):
    template_name = "member/register.html"


class PasswordChangeView(TemplateView):
    template_name = "member/password_change.html"