from django.urls import path

from . import views


app_name = 'payments'


urlpatterns = [
    path(
        'card/<str:frequency>/',
        views.PersonalDetailsView.as_view(),
        name='card_personal_details'
    ),
    path(
        'card/single/pay/',
        views.SingleCardPaymentView.as_view(),
        name='card_details_single'
    ),
    path(
        'card/monthly/pay/',
        views.MonthlyCardPaymentView.as_view(),
        name='card_details_monthly'
    ),
    path(
        'paypal/',
        views.PaypalPaymentView.as_view(),
        name='paypal'
    ),
    path(
        'thank-you/',
        views.ThankYouView.as_view(),
        name='completed'
    ),
]
