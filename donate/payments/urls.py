from django.urls import path

from . import views

app_name = 'payments'


urlpatterns = [
    path('', views.PersonalDetailsView.as_view(), name='personal_details'),
    path('monthly/', views.PersonalDetailsView.as_view(is_monthly=True), name='personal_details_monthly'),
    path('card/', views.SingleCardPaymentView.as_view(), name='card_single'),
    path('monthly/card/', views.MonthlyCardPaymentView.as_view(), name='card_monthly'),
    path('thank-you/', views.ThankYouView.as_view(), name='completed'),
]
