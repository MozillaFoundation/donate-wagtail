from django import template

register = template.Library()


@register.inclusion_tag('fragments/ga_events.html', takes_context=True)
def render_ga_event_data(context):
    return {
        'events': context['request'].session.pop('ga_events', [])
    }
