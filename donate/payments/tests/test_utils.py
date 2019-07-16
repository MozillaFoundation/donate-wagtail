from decimal import Decimal

from django.test import TestCase

from ..utils import freeze_personal_details_for_session


class UtilsTestCase(TestCase):

    def test_freeze_personal_detail_stringifies_decimal_amount(self):
        data = {
            'name': 'Alice',
            'amount': Decimal(50)
        }
        self.assertEqual(freeze_personal_details_for_session(data), {
            'name': 'Alice',
            'amount': '50'
        })
