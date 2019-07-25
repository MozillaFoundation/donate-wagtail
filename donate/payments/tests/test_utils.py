from decimal import Decimal

from django.test import TestCase

from ..utils import freeze_transaction_details_for_session


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
