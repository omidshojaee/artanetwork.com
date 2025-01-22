from django import forms
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _

from mptt.admin import DraggableMPTTAdmin
from taggit.forms import TagField
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
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


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
    search_fields = ('name', 'slug')
    readonly_fields = ('image_preview', 'all_products')
    ordering = ('id',)

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
        'Related products (for this category and its subcategories)'
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-width: 100px; height: auto;" />'
            )
        return _('No image uploaded')

    image_preview.short_description = _('Current image')

    def all_products(self, obj):
        products = Product.objects.filter(
            category__in=obj.get_descendants(include_self=True)
        )

        if not products:
            return _('No products in this category or its subcategories')

        html_content = ""

        for product in products:
            if product.image:
                html_content += format_html(
                    '<div style="display: inline-block; text-align: center; margin: 10px;">'
                    '<img src="{}" style="width: 100px; height: 100px; object-fit: cover;"/>'
                    '<br><span>{}</span>'
                    '<br><span>{}</span>'
                    '</div>',
                    product.image.url,
                    product.category.name,
                    product.name,
                )

        return format_html(html_content)

    all_products.short_description = _('All products in this category')


class CommaSeparatedNumberWidget(forms.TextInput):
    def format_value(self, value):
        if value is None:
            return ''
        return f'{float(value):,}'


class FarsiTagField(TagField):

    def clean(self, value):
        if value:
            value = value.replace('،', ',')

        return super().clean(value)


class ProductAdminForm(forms.ModelForm):

    tags = FarsiTagField(required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].widget = CommaSeparatedNumberWidget(
            attrs={'class': 'form-control', 'style': 'direction: ltr;'}
        )
        self.fields['slug'].widget.attrs.update({'style': 'direction: ltr;'})

    class Media:
        js = ('js/admin_price_format.js',)


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1


class NonEmptyCategoryFilter(admin.SimpleListFilter):
    title = _('category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        # Get categories with their product counts
        categories = (
            Category.objects.annotate(product_count=Count('products'))
            .filter(product_count__gt=0)
            .order_by('tree_id', 'lft')
        )

        # Create choices with proper MPTT indentation and optional count
        choices = []
        for category in categories:
            # Show count only if facets are enabled
            if getattr(self, 'show_facets', False):
                label = f"{category.name} ({category.product_count})"
            else:
                label = f"{category.name}"
            choices.append((str(category.id), label))
        return choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('brand', 'category', 'name', 'slug')}),
        (
            None,
            {
                'fields': (
                    'short_description',
                    'description',
                )
            },
        ),
        (None, {'fields': ('price',)}),
        (None, {'fields': ('tags',)}),
        (None, {'fields': ('image', 'image_preview')}),
        (None, {'fields': ('available', 'guarantee')}),
    )
    form = ProductAdminForm
    inlines = [SpecificationInline]
    list_display = ('name', 'brand', 'category', 'formatted_price', 'tags_list')
    list_filter = ('brand', NonEmptyCategoryFilter, 'tags')
    search_fields = ('name', 'brand__name', 'category__name', 'tags__name')
    autocomplete_fields = ('brand', 'category')
    readonly_fields = ('image_preview',)
    ordering = ('id',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tags_list(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())

    def formatted_price(self, obj):
        return f'{obj.price:,} تومان'

    formatted_price.short_description = _('price in Tomans')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-width: 100px; height: auto;" />'
            )
        return _('No image uploaded')

    image_preview.short_description = _('Current image')
