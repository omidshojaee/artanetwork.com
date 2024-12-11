from django import forms
from django.db import models

# Create your custom fields here.


class CommaIntegerWidget(forms.TextInput):
    class Media:
        js = ('admin/js/comma_formatter.js',)


class CommaIntegerField(models.IntegerField):
    def formfield(self, **kwargs):
        defaults = {'widget': CommaIntegerWidget}
        defaults.update(kwargs)
        return super().formfield(**defaults)
