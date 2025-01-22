from django.db.models import Prefetch

from products.models import Category

# Create your context processors here.


def menu_categories(request):
    return {
        'menu_categories': Category.objects.root_nodes()
        .prefetch_related(
            Prefetch('children', queryset=Category.objects.order_by('id'))
        )
        .order_by('id')
    }
