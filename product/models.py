from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from member.models import Customer
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name=_('ip address'))


def product_image_path_main(instance, filename):
    return f"products/main/{instance.pk}/{filename}"

def image_path(instance, filename):
    return f"products/{instance.product.id}/{filename}"

def category_image_path(instance, filename):
    return f"category/{instance.pk}/{filename}"

class Category(models.Model):
    name = TranslatedField( models.CharField(max_length = 20, db_index = True, verbose_name = _("category name") ))
    slug = models.SlugField(max_length = 70, db_index = True, verbose_name = _("slug"))
    image = models.ImageField(upload_to = category_image_path, blank = True, verbose_name = _("Product Preview"))
    description = TranslatedField(models.TextField(null=True,blank=True, verbose_name=_("Category_description")))

    class Meta:
        ordering = ['name_en']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])



class Product(models.Model):
    category = models.ForeignKey(Category, related_name = 'categories', verbose_name = _("Category"), on_delete = models.PROTECT)
    name = TranslatedField( models.CharField(max_length = 50, db_index = True, verbose_name = _("product name")) )
    slug = models.SlugField(max_length = 100, db_index = True, verbose_name = _("slug"))
    description = TranslatedField( models.TextField(blank = True, verbose_name = _("description")) )
    colors = models.CharField(max_length = 200, verbose_name = _("Colors(delim = ', ')"), blank=True, null=True)
    sizes = models.CharField(max_length = 200, verbose_name = _("Sizes(delim = ', ')"), blank=True, null=True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = _("Price($)"))
    stock = models.PositiveIntegerField(verbose_name = _("In stock"))
    available = models.BooleanField(default = True, verbose_name = _("Available"))
    image_main = models.ImageField(upload_to = product_image_path_main, blank = True, verbose_name = _("image_main"))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _("created"))
    updated = models.DateTimeField(auto_now = True, verbose_name = _("updated"))
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name = _("discount"))
    hits = models.ManyToManyField(IPAddress, through="ProductHits", null=True, blank=True, related_name='visits', verbose_name = _("hits"))
    # like = models.ManyToManyField(Customer, null=True, blank=True, related_name='like')

    class Meta:
        ordering = ['name_en']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def get_total_cost(self):
        return self.price - self.price * (self.discount / Decimal('100'))

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name = 'product', verbose_name = _("Product"), on_delete = models.PROTECT)
    image = models.ImageField(upload_to = image_path, blank = True, verbose_name = _("Image"))
    uploaded = models.DateTimeField(auto_now_add = True, verbose_name = _("uploaded"))
    updated = models.DateTimeField(auto_now = True, verbose_name = _("updated"))

    class Meta:
        ordering = ['updated']
        index_together = [
            ['id', 'image']
        ]
        verbose_name = _('ProductImage')
        verbose_name_plural = _('ProductImages')

    def __str__(self):
        return self.product.name + "_image"


class ProductHits(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = _("product"))
    ip_address = models.ForeignKey(IPAddress,  on_delete = models.CASCADE, verbose_name = _("ip_address"))
    created = models.DateTimeField(auto_now_add = True)
