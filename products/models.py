from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from tinymce.models import HTMLField

# Create your models here.


class Brand(models.Model):
    name = models.CharField(_('brand name'), max_length=100)
    slug = models.SlugField(
        _('brand slug'),
        max_length=100,
        unique=True,
        help_text=_('English letters and numbers only. Replace space with "-".'),
    )
    logo = models.ImageField(
        _('brand logo'), upload_to='brands/', null=True, blank=True
    )

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(_('category name'), max_length=100)
    slug = models.SlugField(
        _('category slug'),
        max_length=100,
        unique=True,
        help_text=_('English letters and numbers only. Replace space with "-.'),
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('parent category'),
        help_text=_(
            'Optional. Select a parent category if this category is a subcategory.'
        ),
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_('product name'), max_length=255)
    slug = models.SlugField(
        _('product slug'),
        max_length=255,
        unique=True,
        help_text=_('English letters and numbers only. Replace space with "-".'),
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('product brand'),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('product category'),
    )
    image = models.ImageField(
        _('product image'), upload_to='products/', null=True, blank=True
    )
    description = HTMLField(_('product description'))
    price = models.IntegerField(_('product price'), help_text=_('Price in Toman.'))
    tags = TaggableManager(_('product tags'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name


class Specification(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='specifications'
    )
    key = models.CharField(
        _('spec title'), max_length=255, help_text=_('e.g. Color, Size, etc.')
    )
    value = models.CharField(
        _('spec value'), max_length=255, help_text=_('e.g. Red, 42, etc.')
    )

    class Meta:
        verbose_name = _('specification')
        verbose_name_plural = _('specifications')

    def __str__(self):
        return f'{self.key}: {self.value}'
