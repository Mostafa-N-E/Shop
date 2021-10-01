from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import View

from product.models import Product
from basket.views import Basket
from member.models import Customer


class OrderView(View):
    template_name = 'order/order.html'

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        basket = Basket(request)
        products = [int(key) for key in basket.basket.keys() ]
        products_num = { int(id):basket.basket[str(id)]['number'] for id in products }
        price = {'get_total_price':basket.get_total_price(), 'get_discount':basket.get_discount(),
                 'get_total_price_after_discount':basket.get_total_price_after_discount()}
        context={'basket':Product.objects.filter(id__in=products), 'price':price, 'products_num':products_num, 'customer':customer}
        return render(request, self.template_name, context=context)