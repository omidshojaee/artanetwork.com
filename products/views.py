from django.views.generic import DetailView, ListView

from .models import Category, Product

# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        return Product.objects.filter(category__slug=category_slug)
