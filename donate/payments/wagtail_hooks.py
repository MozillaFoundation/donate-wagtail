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
