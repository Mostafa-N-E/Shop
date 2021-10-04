from django.shortcuts import render
from .models import Customer
# Create your views here.
from django.views import generic
from django.views.generic import TemplateView, UpdateView
from order.models import Order

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
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        recent_orders = Order.objects.all().order_by('-order_base__created')[:5]
        return render(request, "member/customer/profile.html", {'customer': customer,'recent_orders': recent_orders,})


class Profile_edit(UpdateView):
    model = Customer
    fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'phone_number', 'gender', 'address', 'postal_code', 'city',]
    # form_class = CustomerForm
    template_name = 'member/customer/edit_info.html'

    def get_success_url(self):
        self.success_url = f'http://127.0.0.1:8000/member/profile/{self.request.user.id}'

