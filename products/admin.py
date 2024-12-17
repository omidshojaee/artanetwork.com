from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from mptt.admin import DraggableMPTTAdmin

from .models import Brand, Category

# Register your models here.


class BrandAdminForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['slug'].widget.attrs.update({'style': 'direction: ltr;'})

        if self.instance and self.instance.logo:
            self.fields['logo'].help_text = mark_safe(
                f'<img src="{self.instance.logo.url}" alt="{self.instance.name}" style="width: 100px; height: auto; margin-top: 10px;" />'
            )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    form = BrandAdminForm
    list_display = ('name', 'logo_thumbnail')
    search_fields = ('name',)

    def logo_thumbnail(self, obj):
        return mark_safe(
            f'<img src="{obj.logo.url}" alt="{obj.name}" style="width: 100px; height: auto;" />'
        )

    logo_thumbnail.short_description = _('logo thumbnail')


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['slug'].widget.attrs.update({'style': 'direction: ltr;'})


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    form = CategoryAdminForm
    list_display = (
        'tree_actions',
        'indented_title',
    )
    list_display_links = ('indented_title',)
    search_fields = ('name',)
