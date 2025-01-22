from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Slider(models.Model):
    title = models.CharField(_('slider title'), max_length=100)
    subtitle = models.CharField(_('slider subtitle'), max_length=255)
    image = models.ImageField(
        _('slider image'), upload_to='slider/', null=True, blank=True
    )

    class Meta:
        verbose_name = _('slider')
        verbose_name_plural = _('sliders')

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(_('contact name'), max_length=100)
    tel = models.CharField(_('contact email'), max_length=20)
    subject = models.CharField(_('contact subject'), max_length=100)
    message = models.TextField(_('contact message'))
    ip = models.GenericIPAddressField(_('contact ip'), null=True, blank=True)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    email = models.EmailField(_('newsletter email'), max_length=100)
    ip = models.GenericIPAddressField(_('newsletter ip'), null=True, blank=True)

    class Meta:
        verbose_name = _('newsletter')
        verbose_name_plural = _('newsletters')

    def __str__(self):
        return self.email
