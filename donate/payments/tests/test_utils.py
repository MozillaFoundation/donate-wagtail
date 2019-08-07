from decimal import Decimal

from django.test import TestCase

from ..utils import (
    freeze_transaction_details_for_session, get_default_currency, get_suggested_monthly_upgrade
)


class UtilsTestCase(TestCase):

    def test_freeze_transaction_details_stringifies_decimal_amount(self):
        data = {
            'first_name': 'Alice',
            'last_name': 'Bob',
            'amount': Decimal(50)
        }
        self.assertEqual(freeze_transaction_details_for_session(data), {
            'first_name': 'Alice',
            'last_name': 'Bob',
            'amount': '50'
        })

    def test_get_default_currency_uses_map(self):
        self.assertEqual(
            get_default_currency('en-AU;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5'),
            'aud'
        )
        self.assertEqual(
            get_default_currency('en-CA;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5'),
            'cad'
        )

    def test_get_default_currency_next_language_pre(self):
        # First preference is a bogus language. Second one is korean.
        self.assertEqual(
            get_default_currency('fo-FO;q=0.9, ko;q=0.8'),
            'krw'
        )

    def test_get_default_currency_falls_back_to_base_language(self):
        self.assertEqual(
            get_default_currency('es-GG;q=0.9'),
            'eur'
        )

    def test_get_default_currency_fallback_to_usd(self):
        self.assertEqual(get_default_currency(''), 'usd')
        self.assertEqual(get_default_currency('foo'), 'usd')

    def test_get_suggested_monthly_upgrade_from_constant(self):
        self.assertEqual(get_suggested_monthly_upgrade('usd', Decimal(300)), Decimal(30))
        self.assertEqual(get_suggested_monthly_upgrade('usd', Decimal(125)), Decimal(10))
        self.assertEqual(get_suggested_monthly_upgrade('usd', Decimal(35)), Decimal(5))

    def test_get_suggested_monthly_upgrade_small_single_amount(self):
        self.assertIsNone(get_suggested_monthly_upgrade('usd', Decimal(1)))
        self.assertIsNone(get_suggested_monthly_upgrade('aed', Decimal(1)))
