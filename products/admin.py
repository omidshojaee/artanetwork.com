from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from mptt.admin import DraggableMPTTAdmin
from taggit.models import Tag

from .models import Brand, Category, Product, Specification

# Register your models here.


admin.site.unregister(Tag)


class BrandAdminForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['slug'].widget.attrs.update({'style': 'direction: ltr;'})


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    form = BrandAdminForm
    list_display = ('name', 'logo_thumbnail')
    search_fields = ('name',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.logo:
            return mark_safe(
                f'<img src="{obj.logo.url}" style="max-width: 100px; height: auto;" />'
            )
        return _('No image uploaded')

    image_preview.short_description = _('Current image')

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
        'related_products_count',
        'related_products_cumulative_count',
    )
    list_display_links = ('indented_title',)
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        qs = Category.objects.add_related_count(
            qs, Product, 'category', 'products_cumulative_count', cumulative=True
        )

        qs = Category.objects.add_related_count(
            qs, Product, 'category', 'products_count', cumulative=False
        )

        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = _(
        'Related products (for this specific category)'
    )

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = _(
        'Related products (in this category and its subcategories)'
    )


class CommaSeparatedNumberWidget(forms.TextInput):
    def format_value(self, value):
        if value is None:
            return ''
        return f'{value:,}'


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['price'].widget = CommaSeparatedNumberWidget(
            attrs={'class': 'form-control', 'style': 'direction: ltr;'}
        )

    class Media:
        js = ('js/admin_price_format.js',)


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [SpecificationInline]
    list_display = ('name', 'brand', 'category', 'formatted_price', 'tags_list')
    search_fields = ('name', 'brand__name', 'category__name', 'tags__name')
    autocomplete_fields = ('brand', 'category')
    readonly_fields = ('image_preview',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tags_list(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())

    def formatted_price(self, obj):
        return f'{obj.price:,} تومان'

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-width: 100px; height: auto;" />'
            )
        return _('No image uploaded')

    image_preview.short_description = _('Current image')

    formatted_price.short_description = _('formatted price')
