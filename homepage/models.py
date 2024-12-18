from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Slider(models.Model):
    title = models.CharField(_('slide title'), max_length=100)
    subtitle = models.CharField(_('slide subtitle'), max_length=255)
    image = models.ImageField(
        _('slide image'), upload_to='slider/', null=True, blank=True
    )

    class Meta:
        verbose_name = _('slider')
        verbose_name_plural = _('sliders')

    def __str__(self):
        return self.title
