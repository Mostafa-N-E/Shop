from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import View
from django.views.generic import UpdateView, DetailView, ListView, CreateView, DeleteView

from .models import Order, OrderItem, BaseOrder
from product.models import Product
from basket.views import Basket
from member.models import Customer

from django.contrib.auth.mixins import LoginRequiredMixin

class OrderView(LoginRequiredMixin,View):
    template_name = 'order/order.html'
    login_url = "/member/login/"

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        basket = Basket(request)
        products = [int(key) for key in basket.basket.keys()]
        products_num = {int(id): basket.basket[str(id)]['number'] for id in products}
        price = {'get_total_price': basket.get_total_price(), 'get_discount': basket.get_discount(),
                 'get_total_price_after_discount': basket.get_total_price_after_discount()}
        context = {'basket': Product.objects.filter(id__in=products), 'price': price, 'products_num': products_num,
                   'customer': customer}
        return render(request, self.template_name, context=context)


# class RecentOrder(ListView):
#     model = OrderItem
#     context_object_name = 'orders'
#     template_name = 'order/list_orders.html'
#
#     def get(self, request, *args, **kwargs):
#         orders = OrderItem.objects.all().order_by('-order__created')[:5]
#         context={'orders':orders, }
#         return render(request, self.template_name, context=context)


class ListOrder(LoginRequiredMixin,ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/orders.html'
    login_url = "/member/login/"

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        orders = Order.objects.filter(order_base__customer=customer).order_by('-order_base__created')
        return render(request, self.template_name, context={'orders': orders,})


class DetailOrder(LoginRequiredMixin,DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order/order_detail.html'
    login_url = "/member/login/"

    # def get(self, request, *args, **kwargs):
    #     order = Order.objects.get(pk=self.kwargs['pk'])
    #     return render(request, self.template_name, context={'order': order,})


class CreateOrder(LoginRequiredMixin,CreateView):
    model = OrderItem
    login_url = "/member/login/"
    # template_name = 'order/create_order.html'

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        basket = Basket(request)
        products_id = [int(key) for key in basket.basket.keys()]
        products = Product.objects.filter(id__in=products_id)
        base_order = BaseOrder(customer=customer)
        base_order.save()
        order_items = []
        for product in products:
            order_item = OrderItem(
                product=product
                , quantity=basket.basket[str(product.id)]['number']
            )
            order_item.save()
            order_items.append(order_item)

        order = Order.objects.create(order_base=base_order)
        order.save()
        for product in order_items:
            order.order_items.add(product)
            order.save()

        # order = Order(customer=customer, order_items=OrderItem.objects.filter(id__in=order_items))
        # order.save()
        return HttpResponse("created")


class DeleteOrder(LoginRequiredMixin,DeleteView):
    model = BaseOrder
    login_url = "/member/login/"


# class UpdateOrder(UpdateView):
#     model = Order
#     fields = []
#     template_name = 'order/update_order.html'



