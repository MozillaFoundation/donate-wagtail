from decimal import Decimal

from django.test import TestCase

from ..utils import freeze_transaction_details_for_session, get_suggested_monthly_upgrade


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

    def test_get_suggested_monthly_upgrade_from_constant(self):
        self.assertEqual(get_suggested_monthly_upgrade('usd', Decimal(300)), Decimal(30))
        self.assertEqual(get_suggested_monthly_upgrade('usd', Decimal(125)), Decimal(10))
        self.assertEqual(get_suggested_monthly_upgrade('usd', Decimal(35)), Decimal(5))

    def test_get_suggested_monthly_upgrade_default(self):
        # AED has no monthly suggestions, so we should default to 10% rounded up
        self.assertEqual(get_suggested_monthly_upgrade('aed', Decimal(156)), Decimal(16))
        # USD has suggestins, but this value is below the smallest suggestion tier, so we
        # should default to 10% rounded up
        self.assertEqual(get_suggested_monthly_upgrade('usd', Decimal(11)), Decimal(2))
