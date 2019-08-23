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

    def test_get_default_currency_matches_exact_locale(self):
        self.assertEqual(get_default_currency('nb-NO'), 'nok')

    def test_get_default_currency_falls_back_to_base_language(self):
        self.assertEqual(get_default_currency('es-GG'), 'eur')

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
