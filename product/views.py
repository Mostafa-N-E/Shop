from django.shortcuts import render, redirect
from django.views import generic

from .models import Product, Category, ProductImage
from django.utils.translation import activate

from django.db.models import Count, Q,Case, When, IntegerField
from datetime import datetime, timedelta

from django.core.paginator import Paginator

class Products(generic.ListView):
    model = Product
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        last_month = datetime.today() - timedelta(days=30)
        products = Product.objects.all().annotate(
            count=Count('hits', filter=Q(producthits__created__gt =last_month))
        ).order_by('-count')
        # contact_list = Contact.objects.all()
        paginator = Paginator(products, 5)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        products_list = paginator.get_page(page_number)

        categories = Category.objects.all()
        context = {'products_list': products_list, 'categories': categories, }
        return render(request, 'home.html', context)


class Category_Products(generic.ListView):
    model = Product
    template_name = 'product/products__category.html'

    def get(self, request, *args, **kwargs):
        last_month = datetime.today() - timedelta(days=30)
        slug = self.kwargs['slug']
        products = Product.objects.filter(category__slug=slug)
        paginator = Paginator(products, 5)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        products_list = paginator.get_page(page_number)
        category = Category.objects.get(slug=slug)
        context = {'products_list': products_list, 'category': category, }
        return render(request, 'product/products__category.html', context)


class ProductDetail(generic.DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=self.kwargs['pk'])
        ip_address = self.request.user.ip_address
        if ip_address not in product.hits.all():
            product.hits.add(ip_address)
        product_images = ProductImage.objects.filter(product=product)
        context = {'product': product, 'product_images': product_images, }
        return render(request, 'product/product_detail.html', context)


def change_lang(request):
    activate(request.GET.get('lang'))
    return redirect(request.GET.get('next'))
