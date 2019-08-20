from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from . import constants


class StartCardPaymentForm(forms.Form):
    amount = forms.DecimalField(min_value=0.01, decimal_places=2)
    currency = forms.ChoiceField(choices=constants.CURRENCY_CHOICES)
    source_page_id = forms.IntegerField(widget=forms.HiddenInput)


class BraintreePaymentForm(forms.Form):
    braintree_nonce = forms.CharField(widget=forms.HiddenInput)
    amount = forms.DecimalField(min_value=0.01, decimal_places=2, widget=forms.HiddenInput)


class CampaignFormMixin(forms.Form):
    landing_url = forms.URLField(required=False, widget=forms.HiddenInput)
    project = forms.CharField(widget=forms.HiddenInput)
    campaign_id = forms.CharField(required=False, widget=forms.HiddenInput)


class BraintreeCardPaymentForm(CampaignFormMixin, BraintreePaymentForm):
    # max_length on all the fields here is to comply with Braintree validation requirements.
    first_name = forms.CharField(label=_('First name'), max_length=255)
    last_name = forms.CharField(label=_('Last name'), max_length=255)
    email = forms.EmailField(label=_('Email'), max_length=255)
    address_line_1 = forms.CharField(label=_('Street'), max_length=255)
    town = forms.CharField(label=_('Town'), max_length=255)
    post_code = forms.CharField(label=_('ZIP Code'))
    country = CountryField().formfield(initial='US')


class BraintreePaypalPaymentForm(CampaignFormMixin, BraintreePaymentForm):
    frequency = forms.ChoiceField(choices=constants.FREQUENCY_CHOICES, widget=forms.HiddenInput)
    currency = forms.ChoiceField(choices=constants.CURRENCY_CHOICES, widget=forms.HiddenInput)
    source_page_id = forms.IntegerField(widget=forms.HiddenInput)


class CurrencyForm(forms.Form):
    prefix = 'currency-switcher'
    currency = forms.ChoiceField(choices=constants.CURRENCY_CHOICES)


class UpsellForm(forms.Form):
    amount = forms.DecimalField(min_value=1, decimal_places=2, widget=forms.NumberInput(attrs={'step': 'any'}))


class BraintreePaypalUpsellForm(BraintreePaymentForm):
    currency = forms.ChoiceField(choices=constants.CURRENCY_CHOICES, widget=forms.HiddenInput)
    amount = forms.DecimalField(min_value=1, decimal_places=2, widget=forms.NumberInput(attrs={'step': 'any'}))


class NewsletterSignupForm(forms.Form):
    email = forms.EmailField()
    privacy = forms.BooleanField(
        label=mark_safe(_(
            "I'm okay with Mozilla handling my info as explained in this <a %(attrs)s>Privacy Notice</a>."
        ) % {'attrs': 'href="https://www.mozilla.org/privacy/websites/"'})
    )
