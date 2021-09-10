from django.db import models
from product.models import Product
from customer.models import Customer
from cupon.models import Cupon
from decimal import Decimal


class Order(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated', auto_now=True)
    paid = models.BooleanField(verbose_name='Paid', default=False)
    status_code = ((1, 'cancel'),
                   (2, 'success'),
                   (3, 'process'),
                   (4, 'deliver'),
                   (5, 'send'),
                   (6, 'active'))
    status = models.IntegerField(choices=status_code)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order: {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    color = models.CharField(max_length = 200, verbose_name = "Color")
    size = models.CharField(max_length = 200, verbose_name = "Size")
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.product.get_total_cost()


class Basket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    order_items = models.ManyToManyField(OrderItem, related_name='order_items')
    cupon = models.ForeignKey(Cupon, related_name='basket_cupon', null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.customer} -- {self.id}'

    def get_total_cost_of_basket(self):
        total_cost = sum(order_items.get_cost() for order_items in self.order_items.all())
        return total_cost - total_cost * (self.cupon.discount / Decimal('100'))