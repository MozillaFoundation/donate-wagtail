from django.urls import path

from . import views


app_name = 'payments'


urlpatterns = [
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
        'thank-you/',
        views.ThankYouView.as_view(),
        name='completed'
    ),
]
