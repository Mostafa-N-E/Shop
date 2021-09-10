from django.db import  models
from django.contrib.auth import get_user_model
from order.models import OrderItem

User = get_user_model()

GENDER_CHOICES = [
    (1,'Male'),
    (2,'Female'),
]

class Customer(User):
    phone = models.CharField(max_length=15)
    gender = models.PositiveIntegerField(choices=GENDER_CHOICES, db_index = True, verbose_name = "Gender")
    address = models.CharField(verbose_name='Address', max_length=250, null=True, blank=True)  #
    postal_code = models.CharField(verbose_name='Postal Code', max_length=20, null=True, blank=True)   #
    city = models.CharField(verbose_name='City', max_length=100, null=True, blank=True)   #
    # orders = models.ManyToManyField(OrderItem,verbose_name='Customer orders', related_name='customer_orders', null=True, blank=True)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def has_post_info(self):
        customer = Customer.objects.get(email = self.email)
        if customer.address and customer.city and customer.postal_code:
            return True

        return False

    def is_exists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False