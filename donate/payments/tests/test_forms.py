from django import forms
from django.test import TestCase

from .. import constants
from ..forms import MinimumCurrencyAmountMixin


class MinimumCurrencyTestForm(MinimumCurrencyAmountMixin, forms.Form):
    amount = forms.DecimalField()
    currency = forms.ChoiceField(choices=constants.CURRENCY_CHOICES, widget=forms.HiddenInput)
    frequency = forms.ChoiceField(choices=constants.FREQUENCY_CHOICES, widget=forms.HiddenInput)


class MinimumCurrencyAmountMixinTestCase(TestCase):

    def test_init_sets_min_attr_if_currency_supplied(self):
        form = MinimumCurrencyTestForm(initial={'currency': 'usd', 'frequency': constants.FREQUENCY_SINGLE})
        self.assertEqual(form.fields['amount'].widget.attrs['min'], 10)

    def test_clean_validates_minimum_amount(self):
        form = MinimumCurrencyTestForm({'amount': 1, 'currency': 'usd'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'amount': ['Donations must be $10 or more']})
