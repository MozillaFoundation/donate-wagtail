from unittest import mock

from django.conf import settings
from django.test import RequestFactory, TestCase
from django.urls import reverse

from braintree import ErrorCodes, ErrorResult

from ..forms import BraintreePaymentForm
from ..views import BraintreePaymentView, SingleCardPaymentView
from ..exceptions import InvalidAddress


class MockBraintreeTransaction:
    id = 'transaction-id-1'


class MockBraintreeResult:
    is_success = True
    transaction = MockBraintreeTransaction()


class BraintreePaymentTestView(BraintreePaymentView):
    template_name = 'payment/card_single_payment.html'
    success_url = '/'


class BraintreePaymentViewTestCase(TestCase):

    def setUp(self):
        self.details = {
            'name': 'Alice',
            'email': 'alice@example.com',
            'phone_number': '+442088611222',
            'address_line_1': '1 Oak Tree Hill',
            'town': 'New York',
            'post_code': '10022',
            'country': 'US',
            'amount': 50,
        }

        self.request = RequestFactory().get('/')
        self.request.session = self.client.session
        self.view = BraintreePaymentTestView()
        self.view.personal_details = self.details
        self.view.request = self.request

        self.fake_error_result = ErrorResult("gateway", {
            'message': 'Some error',
            'errors': {
                'credit_card': {
                    'errors': [
                        {
                            'code': ErrorCodes.CreditCard.CreditCardTypeIsNotAccepted,
                            'message': 'Type not accepted',
                        },
                        {
                            'code': ErrorCodes.CreditCard.CustomerIdIsInvalid,
                            'message': 'Invalid Customer ID',
                        }
                    ]
                }
            }
        })

    def test_transaction_data_submitted_to_braintree(self):
        form = BraintreePaymentForm({'braintree_nonce': 'hello-braintree', 'payment_mode': 'card'})
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway') as mock_gateway:
            mock_gateway.transaction.sale.return_value = MockBraintreeResult()
            self.view.form_valid(form)

        mock_gateway.transaction.sale.assert_called_once_with({
            'amount': '50.00',
            'billing': {
                'street_address': self.details['address_line_1'],
                'locality': self.details['town'],
                'postal_code': self.details['post_code'],
                'country_code_alpha2': self.details['country'],
            },
            'customer': {
                'email': self.details['email'],
            },
            'custom_fields': {},
            'payment_method_nonce': 'hello-braintree',
            'options': {'submit_for_settlement': True}
        })

    def test_filter_user_card_errors(self):
        filtered = BraintreePaymentTestView().filter_user_card_errors(self.fake_error_result)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0], 'The type of card you used is not accepted.')

    def test_filtered_errors_returned_as_form_errors(self):
        form = BraintreePaymentForm({'braintree_nonce': 'hello-braintree', 'payment_mode': 'card'})
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway') as mock_gateway:
            mock_gateway.transaction.sale.return_value = self.fake_error_result
            response = self.view.form_valid(form)

        self.assertEqual(
            response.context_data['form'].errors,
            {'__all__': ['The type of card you used is not accepted.']}
        )

    def test_generic_error_message_if_no_reportable_errors(self):
        form = BraintreePaymentForm({'braintree_nonce': 'hello-braintree', 'payment_mode': 'card'})
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway') as mock_gateway:
            mock_gateway.transaction.sale.return_value = ErrorResult("gateway", {
                'message': 'Some system error',
                'errors': {}
            })
            response = self.view.form_valid(form)

        self.assertEqual(
            response.context_data['form'].errors,
            {'__all__': ['Sorry there was an error processing your payment. '
                         'Please try again later or use a different card.']}
        )

    def test_generic_paypal_error_message(self):
        form = BraintreePaymentForm({'braintree_nonce': 'hello-braintree', 'payment_mode': 'paypal'})
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway') as mock_gateway:
            mock_gateway.transaction.sale.return_value = ErrorResult("gateway", {
                'message': 'Some system error',
                'errors': {}
            })
            response = self.view.form_valid(form)

        self.assertEqual(
            response.context_data['form'].errors,
            {'__all__': ['Sorry there was an error processing your payment. Please try again.']}
        )

    def test_view_context_on_get(self):
        ctx = self.view.get_context_data()
        self.assertEqual(ctx['braintree_tokenization_key'], settings.BRAINTREE_TOKENIZATION_KEY)

    def test_check_for_address_errors_with_no_address_related_errors(self):
        result = ErrorResult("gateway", {
            'message': 'Some error',
            'errors': {
                'credit_card': {
                    'errors': [
                        {
                            'code': ErrorCodes.CreditCard.CreditCardTypeIsNotAccepted,
                            'message': 'Type not accepted',
                        },
                        {
                            'code': ErrorCodes.CreditCard.CustomerIdIsInvalid,
                            'message': 'Invalid Customer ID',
                        }
                    ]
                }
            }
        })
        view = BraintreePaymentTestView()
        self.assertIsNone(view.check_for_address_errors(result))

    def test_check_for_address_errors_with_address_related_errors(self):
        result = ErrorResult("gateway", {
            'message': 'Some error',
            'errors': {
                'address': {
                    'errors': [
                        {
                            'code': ErrorCodes.Address.PostalCodeInvalidCharacters,
                            'message': 'invalid post code',
                        }
                    ]
                }
            }
        })
        view = BraintreePaymentTestView()
        with self.assertRaises(InvalidAddress):
            view.check_for_address_errors(result)

    def test_gateway_address_errors_triggers_report_invalid_address(self):
        form = BraintreePaymentForm({'braintree_nonce': 'hello-braintree', 'payment_mode': 'card'})
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway') as mock_gateway:
            mock_gateway.transaction.sale.return_value = ErrorResult("gateway", {
                'message': 'Some error',
                'errors': {
                    'address': {
                        'errors': [
                            {
                                'code': ErrorCodes.Address.PostalCodeInvalidCharacters,
                                'message': 'invalid post code',
                            }
                        ]
                    }
                }
            })

            with mock.patch.object(self.view, 'report_invalid_address') as mock_invalid_address:
                self.view.form_valid(form)

        self.assertEqual(mock_invalid_address.call_count, 1)


class SingleCardPaymentViewTestCase(TestCase):

    def setUp(self):
        self.details = {
            'name': 'Alice',
            'email': 'alice@example.com',
            'address_line_1': '1 Oak Tree Hill',
            'town': 'New York',
            'post_code': '10022',
            'country': 'US',
            'amount': 50,
        }

        self.request = RequestFactory().get('/')
        self.request.session = self.client.session
        self.request.session['personal_details'] = self.details
        self.view = SingleCardPaymentView()
        self.view.personal_details = self.details
        self.view.request = self.request

    def test_get_custom_fields(self):
        form = BraintreePaymentForm({'braintree_nonce': 'hello-braintree', 'payment_mode': 'card'})
        assert form.is_valid()
        custom_fields = self.view.get_custom_fields(form)
        self.assertEqual(custom_fields, {})

    def test_session_personal_data_stores_transaction_on_success(self):
        form = BraintreePaymentForm({'braintree_nonce': 'hello-braintree', 'payment_mode': 'card'})
        assert form.is_valid()

        self.view.success(MockBraintreeResult(), form)

        self.assertEqual(
            self.request.session['completed_transaction_details']['transaction_id'],
            'transaction-id-1'
        )
        # personal_details should be removed
        self.assertIsNone(self.request.session.get('personal_details'))

    def test_missing_personal_details_redirects(self):
        response = self.client.get(reverse('payments:card_single'))
        # We can't use assertRedirects here because there is a redirect chain
        # and we only want to test the first redirect.
        self.assertRedirects(response, reverse('payments:personal_details'))

    def test_view_context_on_get(self):
        ctx = self.view.get_context_data()
        self.assertEqual(ctx['payment_amount'], self.details['amount'])

    def test_get_personal_details_url(self):
        url = self.view.get_personal_details_url()
        self.assertEqual(url, '/pay/?amount=50')
