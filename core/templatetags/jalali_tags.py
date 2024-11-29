from django import template

import jdatetime

register = template.Library()


@register.simple_tag
def jalali_now(format_string='%A، %d %B %Y'):
    jalali_date = jdatetime.datetime.now()
    jalali_date_with_locale = jdatetime.datetime(
        year=jalali_date.year,
        month=jalali_date.month,
        day=jalali_date.day,
        hour=jalali_date.hour,
        minute=jalali_date.minute,
        second=jalali_date.second,
        locale=jdatetime.FA_LOCALE,
    )
    formatted_date = jalali_date_with_locale.strftime(format_string)
    english_to_persian = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    formatted_date = formatted_date.translate(english_to_persian)

    return formatted_date
