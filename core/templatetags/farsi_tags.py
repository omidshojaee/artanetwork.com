from django import template

# Register your tags here.

register = template.Library()

english_to_farsi = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


@register.filter(name='to_farsi_digits')
def to_farsi_digits(value):
    return str(value).translate(english_to_farsi)
