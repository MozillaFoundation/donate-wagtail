from wagtail.core.models import Page


def is_donation_page(page_id):
    from .models import CampaignPage, LandingPage   # Avoid circular import
    try:
        page = Page.objects.live().get(pk=page_id).specific
    except Page.DoesNotExist:
        return False

    return page.__class__ in [CampaignPage, LandingPage]


def queue_ga_event(request, event_data):
    if 'ga_events' in request.session:
        request.session['ga_events'].append(event_data)
        request.session.modified = True
    else:
        request.session['ga_events'] = [event_data]
