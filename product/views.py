from django.shortcuts import render
from django.views import generic

from .models import Product, Category

class Products(generic.ListView):
    model = Product
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.all()
        context = {'products': products, 'categories':categories,}
        return render(request, 'base.html', context)



class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'product/product_detail_m.html'
    context_object_name = "product"
