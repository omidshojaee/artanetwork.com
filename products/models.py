from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

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
