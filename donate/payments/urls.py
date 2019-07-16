from django.urls import path

from . import views

app_name = 'payments'


urlpatterns = [
    path('', views.PersonalDetailsView.as_view(), name='personal_details'),
    path('card/', views.SingleCardPaymentView.as_view(), name='card_single'),
    path('thank-you/', views.ThankYouView.as_view(), name='completed'),
]
