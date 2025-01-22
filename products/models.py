from django.db import models
from django.urls import reverse
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
    promotion = models.BooleanField(
        _('promotion'),
        default=False,
        help_text=_('Check this box to display this brand in the promotion section.'),
    )

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'category_slug': self.slug})


class Category(MPTTModel):
    name = models.CharField(_('category name'), max_length=100)
    slug = models.SlugField(
        _('category slug'),
        max_length=100,
        unique=True,
        help_text=_('English letters and numbers only. Replace space with "-".'),
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
    image = models.ImageField(
        _('category image'),
        upload_to='categories/',
        null=True,
        blank=True,
        help_text=_('Upload a category image.'),
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.parent:
            return reverse(
                'products:product_list',
                kwargs={
                    'category_slug': self.parent.slug,
                    'subcategory_slug': self.slug,
                },
            )
        else:
            return reverse(
                'products:subcategory_list',
                kwargs={'category_slug': self.slug},
            )


class Product(models.Model):

    class AvailableChoices(models.TextChoices):
        AVAILABLE = 'available', _('Available')
        UNAVAILABLE = 'unavailable', _('Unavailable')

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
        _('product image'),
        upload_to='products/',
        null=True,
        blank=True,
        help_text=_('Upload a product image.'),
    )
    short_description = models.TextField(
        _('short description'),
        help_text=_('Write a short description for this product.'),
    )
    description = HTMLField(
        _('product description'), help_text=_('Write a description for this product.')
    )
    price = models.IntegerField(
        _('product price'), help_text=_('Enter the price of this product in Tomans.')
    )
    available = models.CharField(
        _('availability'),
        max_length=11,
        choices=AvailableChoices.choices,
        default=AvailableChoices.AVAILABLE,
    )
    guarantee = models.CharField(
        _('product guarantee'),
        max_length=100,
        help_text=_('Determine the guarantee of this product.'),
    )
    tags = TaggableManager(_('product tags'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'products:product_detail',
            kwargs={
                'category_slug': self.category.parent.slug,
                'subcategory_slug': self.category.slug,
                'product_slug': self.slug,
            },
        )


class Specification(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='specifications'
    )
    title = models.CharField(
        _('specification title'),
        max_length=255,
        help_text=_('e.g. Length, Weight, Color, etc.'),
    )
    value = models.CharField(
        _('specification value'),
        max_length=255,
        help_text=_('e.g. 10 cm, 20 kg, Red, etc.'),
    )

    class Meta:
        verbose_name = _('specification')
        verbose_name_plural = _('specifications')

    def __str__(self):
        return f'{self.title} : {self.value}'
