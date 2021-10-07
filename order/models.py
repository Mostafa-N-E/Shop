from django.db import models
from product.models import Product
from member.models import Customer
from cupon.models import Cupon
from decimal import Decimal
from django.utils.translation import gettext_lazy as _


class BaseOrder(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_order', on_delete=models.CASCADE, verbose_name = _("customer"))
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)
    paid = models.BooleanField(verbose_name=_('Paid'), default=False)
    status_code = ((1, _('cancel')),
                   (2, _('success')),
                   (3, _('process')),
                   (4, _('deliver')),
                   (5, _('send')),
                   (6, _('active')))
    status = models.IntegerField(choices=status_code, default=3)

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'Order: {self.id}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='products_order',on_delete=models.CASCADE, verbose_name = _("Color"))
    color = models.CharField(max_length = 200, verbose_name = _("Color"), null=True, blank=True)
    size = models.CharField(max_length = 200, verbose_name = _("Size"), null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.product.get_total_cost()


class Order(models.Model):
    order_base = models.ForeignKey(BaseOrder, related_name='order_base', on_delete=models.CASCADE, verbose_name = _("order base"))
    order_items = models.ManyToManyField(OrderItem, related_name='order_items', verbose_name = _("order items"))
    paymentـtrackingـcode = models.IntegerField(null=True, blank=True, verbose_name = _("payment tracking code")) # for test this field is null

    def __str__(self):
        return f'{self.id}'

    def get_total_cost(self):
        return sum(order_item.product.get_total_cost() for order_item in self.order_items.all())

    def get_number_of_items(self):
        return sum(order_item.quantity for order_item in self.order_items.all())
# class Basket(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
#     order_items = models.ManyToManyField(OrderItem, related_name='order_items')
#     cupon = models.ForeignKey(Cupon, related_name='basket_cupon', null=True, blank=True, on_delete=models.CASCADE)
#
#
#     def __str__(self):
#         return f'{self.customer} -- {self.id}'
#
#     def get_total_cost_of_basket(self):
#         total_cost = sum(order_items.get_cost() for order_items in self.order_items.all())
#         return total_cost - total_cost * (self.cupon.discount / Decimal('100'))