from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Slider

# Register your models here.


class SliderAdminForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.image:
            self.fields['image'].help_text = mark_safe(
                f'<img src="{self.instance.image.url}" alt="{self.instance.title}" style="width: 100px; height: auto; margin-top: 10px;" />'
            )


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    form = SliderAdminForm
    list_display = ('title', 'subtitle', 'image_thumbnail')
    search_fields = ('title', 'subtitle')

    def image_thumbnail(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" alt="{obj.title}" style="width: 100px; height: auto;" />'
        )

    image_thumbnail.short_description = _('image thumbnail')
