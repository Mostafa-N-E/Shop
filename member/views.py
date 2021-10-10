from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Customer, ContactUs
from django.views import generic
from django.views.generic import TemplateView, UpdateView, CreateView
from order.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm


class LoginView(TemplateView):
    """
            Login (this view only render template for LoginAPI) users
    """
    template_name = "member/login.html"

    redirect_field_name = REDIRECT_FIELD_NAME

    def get_redirect_url(self):
        url = self.request.get_full_path().split('=')
        return redirect(url[1])

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if 'next' in self.request.get_full_path():
                return self.get_redirect_url()
            get_lang = self.request.path.split('/')
            return redirect(f'/{get_lang[1]}/home/')
        return render(self.request, self.template_name)


class RegisterView(TemplateView):
    """
            registration (this view only render template for RegistrationAPI) users
    """
    template_name = "member/register.html"


class PasswordChangeView(TemplateView):
    """
            Enable users to change passwords via with this view
            (this view only render template for PasswordChangeAPI)
    """
    template_name = "member/password_change.html"


class PasswordResetView(TemplateView):
    """
            Enable users to recover passwords via email with this view
            (this view only render template for PasswordResetAPI)
    """
    template_name = "member/password_reset.html"


# class ProfileView(TemplateView):
#     template_name = "member/customer/profile.html"

class ProfileView(LoginRequiredMixin, generic.DetailView):
    """
            Enable users visit their information with this view
    """
    model = Customer
    template_name = "member/customer/profile.html"
    login_url = "/member/login/"
    redirect_field_name = "next"

    # raise_exception = True

    def get_object(self, queryset=None):
        customer = Customer.objects.get(pk=self.request.user.id)
        return customer

    def get_context_data(self, **kwargs):
        customer = self.get_object()
        recent_orders = Order.objects.all().order_by('-order_base__created')[:5]
        return {'customer': customer, 'recent_orders': recent_orders, }


class Profile_edit(LoginRequiredMixin, UpdateView):
    """
            Enable users visit their information and edit Items that have access with this view
    """
    model = Customer
    form_class = ProfileForm
    # form_class = CustomerForm
    template_name = 'member/customer/edit_info.html'
    login_url = "/member/login/"

    def get_object(self, queryset=None):
        customer = Customer.objects.get(pk=self.request.user.id)
        return customer

    def get_success_url(self):
        self.success_url = self.request.path
        return self.success_url


