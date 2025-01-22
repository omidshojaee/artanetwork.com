from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Contact, Newsletter, Slider

# Register your models here.


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ('title', 'subtitle')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-width: 200px; height: auto;" />'
            )
        return _('No image uploaded')

    image_preview.short_description = _('Current image')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'tel', 'subject', 'ip')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'ip')
