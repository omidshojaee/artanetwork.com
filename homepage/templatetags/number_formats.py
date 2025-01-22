from django import template

register = template.Library()


@register.filter
def formatted_price(value):
    return '{:,}'.format(value)
