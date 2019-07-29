from django.urls import path

from . import views


app_name = 'payments'


urlpatterns = [
    path(
        'card/thank-you/',
        views.CardUpsellView.as_view(),
        name='card_upsell'
    ),
    path(
        'card/<str:frequency>/',
        views.CardPaymentView.as_view(),
        name='card'
    ),
    path(
        'paypal/',
        views.PaypalPaymentView.as_view(),
        name='paypal'
    ),
    path(
        'paypal/thank-you/',
        views.PaypalUpsellView.as_view(),
        name='paypal_upsell'
    ),
    path(
        'stay-in-touch/',
        views.NewsletterSignupView.as_view(),
        name='newsletter_signup'
    ),
    path(
        'thank-you/',
        views.ThankYouView.as_view(),
        name='completed'
    ),
]
