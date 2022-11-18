from django import template

register = template.Library()


@register.inclusion_tag('fragments/ga_events.html', takes_context=True)
# This tag is used to render GA or datalayer event data on the frontend,
# so it can be picked up by JS.
def render_ga_event_data(context):
    return {
        'events': context['request'].session.pop('ga_events', []),
        'datalayer_event': context['request'].session.pop('datalayer_event', [])
    }
