from decimal import Decimal

from django import template
from django.utils.translation import to_locale

from babel.core import Locale
from babel.numbers import (
    format_currency as babel_format_currency,
    get_currency_symbol
)

from ..constants import LOCALE_MAP

register = template.Library()


def to_known_locale(code):
    code = LOCALE_MAP.get(code, code)
    return to_locale(code)


@register.simple_tag(takes_context=True)
def get_locale(context):
    return to_known_locale(context['request'].LANGUAGE_CODE)


@register.simple_tag(takes_context=True)
def format_currency(context, currency_code, amount):
    locale = to_known_locale(context['request'].LANGUAGE_CODE)
    locale_obj = Locale.parse(locale)
    pattern = locale_obj.currency_formats['standard'].pattern

    # By default, Babel will display a fixed number of decimal places based on the
    # default format for the currency. It doesn't offer any way to tell
    # format_currency to hide decimals for integer values
    # see https://github.com/python-babel/babel/issues/478
    # In order to work around this, we fetch the pattern for the currency in
    # the current locale, and replace a padded decimal with an optional one.
    # We also have to set currency_digits=False otherwise this gets ignored entirely.
    if Decimal(amount) == int(float(amount)):
        pattern = pattern.replace('0.00', '0.##')

    return babel_format_currency(
        amount, currency_code.upper(), format=pattern, locale=locale_obj, currency_digits=False
    )


@register.simple_tag(takes_context=True)
def get_localized_currency_symbol(context, currency_code):
    locale = to_known_locale(context['request'].LANGUAGE_CODE)
    return get_currency_symbol(currency_code.upper(), locale)
