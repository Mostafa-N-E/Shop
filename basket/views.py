from django.shortcuts import render, get_object_or_404, redirect, HttpResponse

# Create your views here.
from django.conf import settings
from django.views import View

from product.models import Product
from decimal import Decimal
from cupon.models import Cupon
from django.utils import timezone
from django.template.defaulttags import register


class Basket(object):
    """

    """
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.CART_SESSION_ID)
        if not basket:
            basket = self.session[settings.CART_SESSION_ID] = {}
        self.basket = basket
        self.cupon_id = self.session.get('cupon_id')

    def add(self, product):
        # def add(self, product, color, size)
        product_id = str(product.id)
        if product_id not in self.basket:
            # self.basket[product_id] = {'price': str(product.price),'color': color,'size': size}
            self.basket[product_id] = {'unit_price': str(product.price), 'number':1}
        else:
            self.basket[product_id]['number'] = self.basket[product_id]['number']+1
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.basket
        self.session.modified = True

    def remove(self, product):
      product_id = str(product.id)
      if product_id in self.basket:
          del self.basket[product_id]
          self.save()

    def low_off(self, product):
      product_id = str(product.id)
      if product_id in self.basket:
          num = self.basket[product_id]['number']
          if num == 1 :
              self.remove(product)
          else:
            self.basket[product_id]['number'] = num-1
          self.save()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.basket[str(product.id)]['product'] = product

        for item in self.basket.values():
            item['unit_price'] = Decimal(item['unit_price'])
            yield item

    def __len__(self):
        return len(self.basket.values())

    def get_total_price(self):
        return sum(float(self.basket[str(id)]['unit_price'])*int(self.basket[str(id)]['number']) for id in self.basket.keys())
        # return sum(Decimal(float(self.basket[str(id)]['unit_price'])*int(self.basket[str(id)]['number'])) for id in self.basket.keys())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def cupon(self):
        if self.cupon_id:
            cupon = Cupon.objects.get(id=self.cupon_id)
            if cupon.active:
                return cupon
        return None

    def get_discount(self):
        if self.cupon:
            return (self.cupon.discount / 100) * self.get_total_price()
            # return (self.cupon.discount / Decimal('100')) * self.get_total_price()
        return 0
        # return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

class BasketView(View):
    """

    """
    # initial = {'key': 'value'}
    template_name = 'basket/basket.html'

    def get(self, request, *args, **kwargs):
        basket = Basket(request)
        products = [int(key) for key in basket.basket.keys() ]
        # products_num = { int(key):basket.basket[str(key)]['number'] for key in basket.basket.keys()}
        products_num = { int(id):basket.basket[str(id)]['number'] for id in products }
        price = {'get_total_price':basket.get_total_price(), 'get_discount':basket.get_discount(),
                 'get_total_price_after_discount':basket.get_total_price_after_discount()}
        context={'basket':Product.objects.filter(id__in=products), 'price':price, 'products_num':products_num, }
        print(context)
        return render(request, self.template_name, context=context)


def basket_add(request):
    # color = request.POST.get('color', None)
    # size = request.POST.get('size', None)
    # Cart(request).add(product=get_object_or_404(Product, id=product_id), color=color, size=size)
    Basket(request).add(product=get_object_or_404(Product, id=request.GET.get('product_id')))
    return redirect(request.META.get('HTTP_REFERER'))

def basket_remove(request):
    Basket(request).remove(
        product=get_object_or_404(Product, id=request.GET.get('product_id')))  # request.GET.keys['product_id']
    return redirect(request.META.get('HTTP_REFERER'))



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_number_of_items(dictionary):
    return sum(dictionary[i] for i in dictionary.keys())