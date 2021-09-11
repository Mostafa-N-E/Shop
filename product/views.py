from django.views import generic

from .models import Product

class Products(generic.ListView):
    model = Product
    template_name = 'product/products.html'
    def get_queryset(self):
        return Product.objects.all()

class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'product/product_detail_m.html'
    context_object_name = "classLesson"
