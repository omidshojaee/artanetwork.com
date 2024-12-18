from django.views.generic import TemplateView

from products.models import Category

from .models import Slider

# Create your views here.


class HomepageView(TemplateView):
    template_name = 'homepage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.all()

        level_one_categories = Category.objects.filter(level=0)

        menu_structure = []

        for category in level_one_categories:
            subcategories = category.get_children()
            menu_structure.append(
                {
                    'level_one': {
                        'name': category.name,
                        'slug': category.slug,
                        'url': (
                            None
                            if subcategories.exists()
                            else f'/products/{category.slug}/'
                        ),
                        'has_children': subcategories.exists(),
                    },
                    'level_two': [
                        {
                            'name': subcategory.name,
                            'slug': subcategory.slug,
                            'url': f'/products/{subcategory.slug}',
                            'has_children': False,
                        }
                        for subcategory in subcategories
                    ],
                }
            )

        context['menu_structure'] = menu_structure

        return context
