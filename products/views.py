from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Category, Product


class SubcategoryListView(ListView):
    model = Category
    template_name = 'products/subcategory_list.html'
    context_object_name = 'subcategories'

    def get_queryset(self):

        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])

        subcategories = category.get_children()

        for subcategory in subcategories:
            subcategory.product_count = subcategory.products.count()

        return subcategories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context['category'] = category
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Get the subcategory based on the slug
        subcategory = get_object_or_404(Category, slug=self.kwargs['subcategory_slug'])

        # Filter products by the subcategory
        return Product.objects.filter(category=subcategory)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = get_object_or_404(Category, slug=self.kwargs['subcategory_slug'])
        context['subcategory'] = subcategory
        context['parent_category'] = subcategory.parent

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_object(self):
        return get_object_or_404(
            Product,
            category__slug=self.kwargs['subcategory_slug'],
            category__parent__slug=self.kwargs['category_slug'],
            slug=self.kwargs['product_slug'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        parent_category = self.object.category.parent

        if parent_category:
            context['related_products'] = (
                Product.objects.filter(category__parent=parent_category)
                .exclude(id=self.object.id)
                .order_by('?')[:10]
            )
        else:
            context['related_products'] = Product.objects.none()

        return context
