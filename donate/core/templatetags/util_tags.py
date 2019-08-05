from decimal import Decimal

from django import template
from django.utils.translation import to_locale

from moneyed import get_currency, Money
from moneyed.localization import format_money, _FORMATTER

register = template.Library()


@register.filter
def is_english(language_code):
    return language_code.startswith('en')


@register.simple_tag(takes_context=True)
def get_locale(context):
    return to_locale(context['request'].LANGUAGE_CODE)


@register.simple_tag(takes_context=True)
def format_currency(context, currency_code, amount):
    locale = to_locale(context['request'].LANGUAGE_CODE)
    currency_obj = get_currency(currency_code.upper())
    amount = Decimal(amount)
    exponent = amount.as_tuple().exponent
    return format_money(Money(amount, currency_obj), locale=locale, decimal_places=-exponent)


@register.simple_tag(takes_context=True)
def get_localized_currency_symbol(context, currency_code):
    locale = to_locale(context['request'].LANGUAGE_CODE)
    prefix, suffix = _FORMATTER.get_sign_definition(currency_code.upper(), locale)
    return prefix.strip() or suffix.strip()
