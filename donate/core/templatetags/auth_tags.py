from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def use_conventional_auth():
    return settings.USE_CONVENTIONAL_AUTH
