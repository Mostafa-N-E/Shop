
from decimal import Decimal

from django.db import models
from member.models import Customer
from order.models import OrderItem
from cupon.models import Cupon

# Create models.

class Basket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    order_items = models.ManyToManyField(OrderItem, related_name='order_items')
    cupon = models.ForeignKey(Cupon, related_name='basket_cupon', null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.customer} -- {self.id}'

    def get_total_cost_of_basket(self):
        total_cost = sum(order_items.get_cost() for order_items in self.order_items.all())
        return total_cost - total_cost * (self.cupon.discount / Decimal('100'))
