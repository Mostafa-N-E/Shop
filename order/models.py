from django.db import models
from product.models import Product
from customer.models import Customer
from cupon.models import Cupon
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated', auto_now=True)
    paid = models.BooleanField(verbose_name='Paid', default=False)
    cupon = models.ForeignKey(Cupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
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

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=5)
    color = models.CharField(max_length = 200, verbose_name = "Color")
    size = models.CharField(max_length = 200, verbose_name = "Size")
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price
