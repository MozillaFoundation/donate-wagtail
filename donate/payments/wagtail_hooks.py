from wagtail.core import hooks
from wagtail_ab_testing.events import BaseEvent


class VisitThankYouPageEvent(BaseEvent):
    name = "Visit the thank you page"
    requires_page = False


@hooks.register('register_ab_testing_event_types')
def register_submit_form_event_type():
    return {
        'visit-thank-you-page': VisitThankYouPageEvent(),
    }


@hooks.register('before_serve_page')
def may_load_card_page(page, request, serve_args, serve_kwargs):
    """
    Make sure users cannot access the card payment page until
    they've been on a wagtail-managed page. This allows us to
    force users to the landing page by virtue of the card
    payment page being a plain Django view.

    If they do try to load the card payment page directly,
    they will get redirected to `/` instead over in the
    views.CardPaymentView.dispatch() functions.

    This value also gets cleared when someone makes a donation,
    so that they can't then immediately fill in a new donation
    form, even if they opened a million tabs first when they
    were allowed to load the card payment page.
    """
    if 'may_load_card_page' not in request.session:
        request.session['may_load_card_page'] = True
