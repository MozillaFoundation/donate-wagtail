from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from django_countries.fields import CountryField

from donate.recaptcha.fields import ReCaptchaField

from . import constants


# Global maximum amount value of 10 million, not currency-specific, intended
# only to put a sane upper limit on all payments.
MAX_AMOUNT_VALUE = 10000000


class StartCardPaymentForm(forms.Form):
    amount = forms.DecimalField(label=_('Amount'), min_value=0.01, max_value=MAX_AMOUNT_VALUE, decimal_places=2)
    currency = forms.ChoiceField(choices=constants.CURRENCY_CHOICES)
    source_page_id = forms.IntegerField(widget=forms.HiddenInput)


class BraintreePaymentForm(forms.Form):
    braintree_nonce = forms.CharField(widget=forms.HiddenInput)
    amount = forms.DecimalField(
        label=_('Amount'), min_value=0.01, max_value=MAX_AMOUNT_VALUE, decimal_places=2,
        widget=forms.HiddenInput
    )


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
    city = forms.CharField(label=_('City'), max_length=255)
    post_code = forms.CharField(
        label=pgettext_lazy(
            "Feel free to replace with “Postal code” or equivalent",
            'ZIP Code'
        )
    )
    country = CountryField(_('Country')).formfield(initial='US')

    if settings.RECAPTCHA_ENABLED:
        captcha = ReCaptchaField()


class BraintreePaypalPaymentForm(CampaignFormMixin, BraintreePaymentForm):
    frequency = forms.ChoiceField(choices=constants.FREQUENCY_CHOICES, widget=forms.HiddenInput)
    currency = forms.ChoiceField(choices=constants.CURRENCY_CHOICES, widget=forms.HiddenInput)
    source_page_id = forms.IntegerField(widget=forms.HiddenInput)

    if settings.RECAPTCHA_ENABLED:
        captcha = ReCaptchaField()


class CurrencyForm(forms.Form):
    prefix = 'currency-switcher'
    currency = forms.ChoiceField(choices=constants.CURRENCY_CHOICES)


class UpsellForm(forms.Form):
    amount = forms.DecimalField(
        label=_('Amount'), min_value=1, max_value=MAX_AMOUNT_VALUE, decimal_places=2,
        widget=forms.NumberInput(attrs={'step': 'any'})
    )


class BraintreePaypalUpsellForm(BraintreePaymentForm):
    currency = forms.ChoiceField(choices=constants.CURRENCY_CHOICES, widget=forms.HiddenInput)
    amount = forms.DecimalField(
        label=_('Amount'), min_value=1, max_value=MAX_AMOUNT_VALUE, decimal_places=2,
        widget=forms.NumberInput(attrs={'step': 'any'})
    )


class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(label=_('Email'))
    privacy = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Because we're rendering HTML into this label, we can't set it at runtime.
        # Django will attempt to translate the string too early if we do.
        self.fields['privacy'].label = mark_safe(_(
            "I’m okay with Mozilla handling my info as explained in this <a href='%(url)s'>Privacy Notice</a>."
        ) % {'url': 'https://www.mozilla.org/privacy/websites/'})
