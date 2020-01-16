from django.urls import path
from django.views.generic.base import RedirectView

app_name = 'thunderbird'


urlpatterns = [
    path(
        'card/thank-you/',
        RedirectView.as_view(pattern_name='payments:newsletter_signup', permanent=False),
        name='card_upsell'
    ),
    path(
        'paypal/thank-you/',
        RedirectView.as_view(pattern_name='payments:newsletter_signup', permanent=False),
        name='paypal_upsell'
    ),
]
