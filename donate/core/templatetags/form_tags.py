from django import template

from wagtail.core.utils import camelcase_to_underscore

register = template.Library()


@register.filter
def widget_type(bound_field):
    return camelcase_to_underscore(bound_field.field.widget.__class__.__name__)


@register.filter
def field_type(bound_field):
    return camelcase_to_underscore(bound_field.field.__class__.__name__)


@register.inclusion_tag('forms/form_field.html')
def render_form_field(field, css_classes=False, front_end_validated=False):
    return {
        'field': field,
        'css_classes': css_classes,
        'front_end_validated': front_end_validated
    }
