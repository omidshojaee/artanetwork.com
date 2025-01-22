from django.db.models import Prefetch
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from products.models import Brand, Category, Product

from .forms import ContactForm, NewsletterForm
from .models import Slider
from .utils import get_client_ip

# Create your views here.


class HomepageView(TemplateView):
    template_name = 'homepage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sliders'] = Slider.objects.all()

        # Get promotional brands and prefetch their products
        promotional_brands = Brand.objects.filter(promotion=True).prefetch_related(
            'products'  # This will efficiently load all products for each brand
        )
        context['promotional_brands'] = promotional_brands

        return context


class ContactView(View):
    def post(self, request, *args, **kwargs):

        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.ip = get_client_ip(request)
            contact.save()
            return JsonResponse(
                {'status': 'success', 'message': 'پیام شما ارسال شد. سپاسگزاریم!'}
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'خطایی رخ داده است. لطفا دوباره تلاش کنید.',
                }
            )


class NewsletterView(View):
    def post(self, request, *args, **kwargs):

        form = NewsletterForm(request.POST)

        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.ip = get_client_ip(request)
            newsletter.save()
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'ایمیل شما با موفقیت ثبت شد. سپاسگزاریم!',
                }
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'خطایی رخ داده است. لطفا دوباره تلاش کنید.',
                }
            )
