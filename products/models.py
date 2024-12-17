from django.db import models
from django.utils.translation import gettext_lazy as _

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
