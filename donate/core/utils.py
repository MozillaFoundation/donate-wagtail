from wagtail.core.models import Page


def is_donation_page(page_id):
    from .models import CampaignPage, LandingPage   # Avoid circular import
    try:
        page = Page.objects.live().get(pk=page_id).specific
    except Page.DoesNotExist:
        return False

    return page.__class__ in [CampaignPage, LandingPage]
