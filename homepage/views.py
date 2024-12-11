from django.views.generic import TemplateView

from products.models import Category

from .models import Slider

# Create your views here.


class HomepageView(TemplateView):
    template_name = 'homepage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.all()
        context['categories'] = Category.objects.all().order_by('id')
        return context
