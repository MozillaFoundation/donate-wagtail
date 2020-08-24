from decimal import Decimal

from django.test import TestCase, override_settings

from ..utils import (
    determine_paypal_account, freeze_transaction_details_for_session, get_default_currency,
    get_merchant_account_id_for_paypal, get_suggested_monthly_upgrade, paypal_macro_fee,
    paypal_micro_fee
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
        self.assertIsNone(get_suggested_monthly_upgrade('brl', Decimal(1)))

    def test_paypal_micro_fee(self):
        self.assertEqual(paypal_micro_fee('usd', Decimal(1)), Decimal('0.11'))

    def test_paypal_macro_fee(self):
        self.assertEqual(paypal_macro_fee('usd', Decimal(1)), Decimal('0.33'))

    def test_determine_paypal_account_micro(self):
        self.assertEqual('micro', determine_paypal_account('usd', Decimal(1)))

    def test_determine_paypal_account_macro(self):
        self.assertEqual('macro', determine_paypal_account('usd', Decimal(20)))

    @override_settings(BRAINTREE_MERCHANT_ACCOUNTS_PAYPAL_MICRO={'usd': 'usdmicro'})
    def test_get_merchant_id_for_paypal_micro(self):
        self.assertEqual(
            get_merchant_account_id_for_paypal('usd', Decimal(1)),
            'usdmicro'
        )

    @override_settings(
        BRAINTREE_MERCHANT_ACCOUNTS={'usd': 'usdmacro'}, BRAINTREE_MERCHANT_ACCOUNTS_PAYPAL_MICRO={}
    )
    def test_get_merchant_id_for_paypal_micro_fallback_to_macro_if_not_set(self):
        self.assertEqual(
            get_merchant_account_id_for_paypal('usd', Decimal(1)),
            'usdmacro'
        )

    @override_settings(
        BRAINTREE_MERCHANT_ACCOUNTS_PAYPAL_MICRO={'usd': 'usdmicro'},
        BRAINTREE_MERCHANT_ACCOUNTS={'usd': 'usdmacro'}
    )
    def test_get_merchant_id_for_paypal_macro(self):
        self.assertEqual(
            get_merchant_account_id_for_paypal('usd', Decimal(20)),
            'usdmacro'
        )
