from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


def product_image_path_main(instance, filename):
    return f"products/main/{instance.pk}/{filename}"

def image_path(instance, filename):
    return f"products/{instance.product.id}/{filename}"


class Category(models.Model):
    name = models.CharField(max_length = 20, db_index = True, verbose_name = "Name")
    slug = models.SlugField(max_length = 70, db_index = True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])



class Product(models.Model):
    category = models.ForeignKey(Category, related_name = 'categories', verbose_name = "Category", on_delete = models.PROTECT)
    name = models.CharField(max_length = 50, db_index = True, verbose_name = "Name")
    slug = models.SlugField(max_length = 100, db_index = True)
    description = models.TextField(blank = True, verbose_name = "Description")
    colors = models.CharField(max_length = 200, verbose_name = "Colors(delim = ', ')", blank=True, null=True)
    sizes = models.CharField(max_length = 200, verbose_name = "Sizes(delim = ', ')", blank=True, null=True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = "Price($)")
    stock = models.PositiveIntegerField(verbose_name = "In stock")
    available = models.BooleanField(default = True, verbose_name = "Available")
    image_main = models.ImageField(upload_to = product_image_path_main, blank = True, verbose_name = "Product Preview")
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def get_total_cost(self):
        return self.price - self.price * (self.discount / Decimal('100'))

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name = 'product', verbose_name = "Product", on_delete = models.PROTECT)
    image = models.ImageField(upload_to = image_path, blank = True, verbose_name = "Image")
    uploaded = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['updated']
        index_together = [
            ['id', 'image']
        ]

    def __str__(self):
        return self.product.name + "_image"