from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField

# Create your models here.


class Slider(models.Model):
    title = models.CharField(_('slider title'), max_length=100)
    subtitle = models.CharField(_('slider subtitle'), max_length=255)
    image = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='slider_image',
        verbose_name=_('slider image'),
    )

    class Meta:
        verbose_name = _('slider')
        verbose_name_plural = _('sliders')

    def __str__(self):
        return self.title
