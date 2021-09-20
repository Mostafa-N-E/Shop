from django.shortcuts import render
from django.views import generic

from .models import Product, Category, ProductImage

class Products(generic.ListView):
    model = Product
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.all()
        context = {'products': products, 'categories':categories,}
        return render(request, 'home.html', context)



class ProductDetail(generic.DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=self.kwargs['pk'])
        product_images = ProductImage.objects.filter(product=product)
        context = {'product': product, 'product_images':product_images,}
        return render(request, 'product/product_detail_m.html', context)