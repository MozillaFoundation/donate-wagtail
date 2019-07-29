from django import template

register = template.Library()


@register.filter
def is_english(language_code):
    return language_code.startswith('en')
