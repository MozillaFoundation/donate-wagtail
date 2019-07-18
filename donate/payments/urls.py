from django.urls import path

from . import constants, views


app_name = 'payments'


urlpatterns = [
    path(
        '<str:method>/<str:frequency>/',
        views.PersonalDetailsView.as_view(),
        name='personal_details'
    ),
    path(
        'card/single/pay/',
        views.SinglePaymentView.as_view(method=constants.METHOD_CARD),
        name='card_single'
    ),
    path(
        'card/monthly/pay/',
        views.MonthlyPaymentView.as_view(method=constants.METHOD_CARD),
        name='card_monthly'
    ),
    path(
        'paypal/single/pay/',
        views.SinglePaymentView.as_view(method=constants.METHOD_PAYPAL),
        name='paypal_single'
    ),
    path(
        'paypal/monthly/pay/',
        views.MonthlyPaymentView.as_view(method=constants.METHOD_PAYPAL),
        name='paypal_monthly'
    ),
    path(
        'thank-you/',
        views.ThankYouView.as_view(),
        name='completed'
    ),
]
