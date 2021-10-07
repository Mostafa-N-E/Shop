from django.db import  models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField

User = get_user_model()


class ContactUs(models.Model):
    name = models.CharField(max_length=50, verbose_name = _("contact_name"))
    subject = models.CharField(max_length=50, verbose_name = _("contact_subject"))
    email = models.EmailField(verbose_name=_('contact_email'))
    message = models.TextField(verbose_name = _("contact_message"))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        verbose_name = _('ContactUs')
        verbose_name_plural = _('ContactUs')


# --------------------------------------------------CUSTOMER----------------------------------------------------------

GENDER_CHOICES = [
    (1,'Male'),
    (2,'Female'),
]

class Customer(User):
    phone_number = models.CharField(max_length=15, verbose_name = _("phone_number"),null=True, blank=True)
    gender = models.PositiveIntegerField(choices=GENDER_CHOICES, db_index = True, verbose_name = _("Gender"),null=True, blank=True)
    address = models.CharField(verbose_name=_('Address'), max_length=250, null=True, blank=True)  #
    postal_code = models.CharField(verbose_name=_('Postal Code'), max_length=20, null=True, blank=True)   #
    city = models.CharField(verbose_name=_('City'), max_length=100, null=True, blank=True)   #
    # orders = models.ManyToManyField(OrderItem,verbose_name='Customer orders', related_name='customer_orders', null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

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

# -----------------------------------------------------STAFF----------------------------------------------------------



# -----------------------------------------------------MANAGER----------------------------------------------------------
