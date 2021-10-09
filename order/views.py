from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from .models import Order, OrderItem, BaseOrder
from product.models import Product
from basket.views import Basket
from member.models import Customer
from django.template.defaulttags import register
from django.contrib.auth.mixins import LoginRequiredMixin
from cupon.models import Cupon

class OrderView(LoginRequiredMixin, View):
    """

    """
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


class ListOrder(LoginRequiredMixin, ListView):
    """

    """
    model = Order
    context_object_name = 'orders'
    template_name = 'order/orders.html'
    login_url = "/member/login/"

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        orders = Order.objects.filter(order_base__customer=customer).order_by('-order_base__created')
        # orders_filter_by_status = {i+1:Order.objects.filter(order_base__customer=customer).filter(order_base__status=i).count() for i in range(BaseOrder.status_code.__len__())}
        return render(request, self.template_name, context={'orders': orders, })


class DetailOrder(LoginRequiredMixin, DetailView):
    """

    """
    model = Order
    context_object_name = 'order'
    template_name = 'order/order_detail.html'
    login_url = "/member/login/"


class CreateOrder(LoginRequiredMixin, CreateView):
    """

    """
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
        if basket.cupon_id:
            cupon = Cupon.objects.get(code=basket.cupon_id)
            request.session['cupon_id'] = None
            cupon.is_used = True
            cupon.save()
        basket.clear()
        return HttpResponse(status=201) #,"created"


class DeleteOrder(LoginRequiredMixin, DeleteView):
    """

    """
    model = BaseOrder
    login_url = "/member/login/"


def apply_cupon(request):
    """

    """
    if request.method == 'POST':
        cupon_id = request.POST.get('cupon_id')
        try:
            cupon = Cupon.objects.get(code=cupon_id)
            if cupon.active and ( not cupon.is_used ):
                request.session['cupon_id'] = cupon_id
                return HttpResponse(status=200)
            else:
                return HttpResponseNotFound("Your discount code has expired")
        except:
            return HttpResponseNotFound("This cupon ID invalid")
    else:
        return HttpResponseForbidden()


@register.filter
def get_range(int):
    """

    """
    return range(1, int + 1)


@register.filter
def get_number_of_order(status, customer_id):
    """

    """
    return Order.objects.filter(order_base__customer_id=customer_id).filter(order_base__status=status).count()

# class UpdateOrder(UpdateView):
#     model = Order
#     fields = []
#     template_name = 'order/update_order.html'
