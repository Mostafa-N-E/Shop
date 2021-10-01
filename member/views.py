from django.shortcuts import render
from .models import Customer
# Create your views here.
from django.views import generic
from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = "member/login.html"


class RegisterView(TemplateView):
    template_name = "member/register.html"


class PasswordChangeView(TemplateView):
    template_name = "member/password_change.html"


class PasswordResetView(TemplateView):
    template_name = "member/password_reset.html"


# class ProfileView(TemplateView):
#     template_name = "member/customer/profile.html"

class ProfileView(generic.DetailView):
    model = Customer

    def get(self, request, *args, **kwargs):
        print("-------------------------------------")
        print(self.kwargs['pk'])
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        return render(request, "member/customer/profile.html", {'customer': customer,})