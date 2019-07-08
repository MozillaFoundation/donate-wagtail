from django import template

from donate.navigation.models import NavigationSettings

register = template.Library()


# Primary nav snippets
@register.inclusion_tag('tags/primarynav.html', takes_context=True)
def primarynav(context):
    request = context['request']
    return {
        'primarynav': NavigationSettings.for_site(request.site).primary_navigation,
        'request': request,
    }
