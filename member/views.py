from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render, redirect
from .models import Customer
from django.views import generic
from django.views.generic import TemplateView, UpdateView, View
from order.models import Order

from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(TemplateView):
    template_name = "member/login.html"

    redirect_field_name = REDIRECT_FIELD_NAME

    def get_redirect_url(self):
        url = self.request.get_full_path().split('=')
        return redirect(url[1])

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if 'next' in self.request.get_full_path():
                return self.get_redirect_url()
            return redirect('/products/home/')
        return render(self.request, self.template_name)




class RegisterView(TemplateView):
    template_name = "member/register.html"


class PasswordChangeView(TemplateView):
    template_name = "member/password_change.html"


class PasswordResetView(TemplateView):
    template_name = "member/password_reset.html"


# class ProfileView(TemplateView):
#     template_name = "member/customer/profile.html"

class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Customer
    template_name = "member/customer/profile.html"
    login_url = "/member/login/"
    redirect_field_name = "next"
    # raise_exception = True

    def get_context_data(self, **kwargs):
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        recent_orders = Order.objects.all().order_by('-order_base__created')[:5]
        return {'customer': customer,'recent_orders': recent_orders,}


class Profile_edit(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'phone_number', 'gender', 'address', 'postal_code', 'city',]
    # form_class = CustomerForm
    template_name = 'member/customer/edit_info.html'
    login_url = "/member/login/"

    def get_success_url(self):
        self.success_url = f'http://127.0.0.1:8000/member/profile/{self.request.user.id}'

