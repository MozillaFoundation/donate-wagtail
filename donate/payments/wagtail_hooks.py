from wagtail.core import hooks
from wagtail_ab_testing.events import BaseEvent
from donate.core.models import LandingPage


class VisitThankYouPageEvent(BaseEvent):
    name = "Visit the thank you page"

    def get_page_types(self):
        return [LandingPage]


@hooks.register('register_ab_testing_event_types')
def register_submit_form_event_type():
    return {
        'visit-thank-you-page': VisitThankYouPageEvent(),
    }
