from django import forms
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from . import constants


class PersonalDetailsForm(forms.Form):
    # max_length on all the fields here is to comply with Braintree validation requirements.
    first_name = forms.CharField(label=_('First name'), max_length=255)
    last_name = forms.CharField(label=_('Last name'), max_length=255)
    email = forms.EmailField(label=_('Email'), max_length=255)
    address_line_1 = forms.CharField(label=_('Street'), max_length=255)
    town = forms.CharField(label=_('Town'), max_length=255)
    post_code = forms.CharField(label=_('ZIP Code'))
    country = CountryField().formfield(initial='US')
    amount = forms.DecimalField(min_value=0.01, decimal_places=2, widget=forms.HiddenInput)


class BraintreePaymentForm(forms.Form):
    braintree_nonce = forms.CharField(widget=forms.HiddenInput)
    amount = forms.DecimalField(min_value=0.01, decimal_places=2, widget=forms.HiddenInput)


class BraintreePaypalPaymentForm(BraintreePaymentForm):
    frequency = forms.ChoiceField(choices=constants.FREQUENCY_CHOICES, widget=forms.HiddenInput)
