from django.contrib import admin
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

from mptt.admin import DraggableMPTTAdmin

from .custom_fields import CommaIntegerField, CommaIntegerWidget
from .models import Category, Product, Specification

# Register your models here.


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'related_products_count',
        'related_products_cumulative_count',
    )
    list_display_links = ('indented_title',)

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
        'Related products (in this category and its children)'
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (SpecificationInline,)
    list_display = ('name', 'category', 'in_stock')
    search_fields = ('name', 'category__name', 'tags__name')
    formfield_overrides = {CommaIntegerField: {'widget': CommaIntegerWidget}}
