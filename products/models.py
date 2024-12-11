from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from tinymce.models import HTMLField

from .custom_fields import CommaIntegerField

# Create your models here.


class Category(MPTTModel):
    name = models.CharField(_('category name'), max_length=100)
    slug = models.SlugField(_('category slug'), unique=True)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = 'name'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_('product_name'), max_length=255)
    slug = models.SlugField(_('product slug'), unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('category'),
    )
    image = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='product_image',
        verbose_name=_('product image'),
    )
    description = HTMLField(_('product description'))
    in_stock = models.BooleanField(_('in stock'), default=False)
    price = CommaIntegerField(_('price'), default=0)
    tags = TaggableManager(_('tags'), blank=True)


class Specification(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='specifications'
    )
    key = models.CharField(_('spec name'), max_length=255)
    value = models.CharField(_('spec value'), max_length=255)

    def __str__(self):
        return f'{self.key}: {self.value}'
