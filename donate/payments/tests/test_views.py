from datetime import date
from decimal import Decimal
from unittest import mock

from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.views.generic import FormView

from braintree import ErrorCodes, ErrorResult
from freezegun import freeze_time
from freezegun.api import FakeDate

from ..forms import (
    BraintreePaymentForm, BraintreeCardPaymentForm, BraintreePaypalPaymentForm,
    BraintreePaypalUpsellForm, UpsellForm
)
from ..tasks import send_transaction_to_basket
from ..views import (
    BraintreePaymentMixin, CardPaymentView, CardUpsellView, NewsletterSignupView,
    PaypalPaymentView, PaypalUpsellView, TransactionRequiredMixin
)
from ..exceptions import InvalidAddress


class MockPaypalDetails:
    payer_email = 'customer@example.com'
    payer_first_name = 'Bob'
    payer_last_name = 'Jones'


class MockBraintreeTransaction:
    id = 'transaction-id-1'
    disbursement_details = mock.MagicMock()
    disbursement_details.settlement_amount = Decimal(10)
    paypal_details = MockPaypalDetails()
    payment_instrument_type = 'credit_card'
    credit_card_details = mock.MagicMock()
    credit_card_details.card_type = 'Visa'


class MockBraintreeResult:
    is_success = True
    transaction = MockBraintreeTransaction()


class MockBraintreeSubscription:
    id = 'subscription-id-1'


class MockBraintreePaymentMethod:
    token = 'payment-method-1'
    last_4 = '1234'
    email = 'test@example.com'
    payer_info = {
        'first_name': 'Bob',
        'last_name': 'Jones'
    }
    card_type = 'Visa'


class MockBraintreeCustomer:
    email = 'customer@example.com'
    last_name = 'Jones'
    payment_methods = [
        MockBraintreePaymentMethod()
    ]


class MockBraintreeSubscriptionResult:
    is_success = True
    subscription = MockBraintreeSubscription()


class BraintreeMixinTestView(BraintreePaymentMixin, FormView):

    def get_transaction_details_for_session(self, result, form):
        return {
            'amount': '50',
        }


class BraintreeMixinTestCase(TestCase):

    def test_success_stores_transaction_details_to_session(self):
        form = BraintreePaymentForm({'braintree_nonce': 'hello-braintree', 'amount': 10})
        assert form.is_valid()

        view = BraintreeMixinTestView()
        view.request = RequestFactory().get('/')
        view.request.session = {
            'landing_url': 'http://localhost',
            'project': 'thunderbird',
            'campaign_id': 'piday',
        }
        view.request.LANGUAGE_CODE = 'en-US'
        view.handle_successful_transaction(MockBraintreeResult(), form, send_data_to_basket=False)

        self.assertEqual(view.request.session['completed_transaction_details'], {
            'amount': '50',
            'locale': 'en-US',
            'landing_url': 'http://localhost',
            'project': 'thunderbird',
            'campaign_id': 'piday',
        })

    def test_queue_ga_transaction(self):
        view = BraintreeMixinTestView()
        view.request = RequestFactory().get('/')
        view.request.session = self.client.session
        with mock.patch('donate.payments.views.queue_ga_event', autospec=True) as mock_queue:
            view.queue_ga_transaction('trans-id', 'usd', Decimal(50), 'Card', 'Donation')
        self.assertEqual(mock_queue.call_count, 3)
        mock_queue.assert_any_call(view.request, [
            'ecommerce:addTransaction', {
                'id': 'trans-id',
                'revenue': '50',
                'currency': 'USD',
                'affiliation': '',
            }
        ])
        mock_queue.assert_any_call(view.request, [
            'ecommerce:addItem', {
                'id': 'trans-id',
                'name': 'Card',
                'sku': 'Card',
                'category': 'Donation',
                'price': '50',
                'quantity': '1',
            }
        ])
        mock_queue.assert_any_call(view.request, ['ecommerce:send'])


class CardPaymentViewTestCase(TestCase):

    def setUp(self):
        self.form_data = {
            'first_name': 'Alice',
            'last_name': 'Bob',
            'email': 'alice@example.com',
            'address_line_1': '1 Oak Tree Hill',
            'city': 'New York',
            'post_code': '10022',
            'country': 'US',
            'amount': Decimal(50),
            'braintree_nonce': 'hello-braintree',
            'landing_url': 'http://localhost',
            'project': 'mozillafoundation',
            'campaign_id': 'pi_day',
            'device_data': '{"some": "data"}'
        }

        self.request = RequestFactory().get('/')
        self.request.session = self.client.session
        self.request.LANGUAGE_CODE = 'en-US'
        self.view = CardPaymentView()
        self.view.payment_frequency = 'single'
        self.view.currency = 'usd'
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

    def test_404_for_invalid_frequency(self):
        request = RequestFactory().get('/')
        view = CardPaymentView()
        view.request = request
        with self.assertRaises(Http404):
            view.dispatch(request, frequency='yearly')

    def test_bad_amount_redirects(self):
        request = RequestFactory().get('/?amount=foo')
        view = CardPaymentView()
        view.request = request
        response = view.dispatch(request, frequency='monthly')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')

    def test_filter_user_card_errors(self):
        filtered = CardPaymentView().filter_user_card_errors(self.fake_error_result)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0], 'The type of card you used is not accepted.')

    def test_filtered_errors_returned_as_form_errors(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()

        self.view.process_braintree_error_result(self.fake_error_result, form)
        self.assertEqual(
            form.errors,
            {'__all__': ['The type of card you used is not accepted.']}
        )

    def test_generic_error_message_if_no_reportable_errors(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()

        self.view.process_braintree_error_result(ErrorResult("gateway", {
            'message': 'Some system error',
            'errors': {}
        }), form)

        self.assertEqual(
            form.errors,
            {'__all__': ['Sorry there was an error processing your payment. '
                         'Please try again later or use a different payment method.']}
        )

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
        view = CardPaymentView()
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
        view = CardPaymentView()
        with self.assertRaises(InvalidAddress):
            view.check_for_address_errors(result)

    def test_gateway_address_errors_triggers_report_invalid_address(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()

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

        self.view.process_braintree_error_result(result, form)
        self.assertEqual(len(self.view.gateway_address_errors), 1)

    def test_get_custom_fields(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()
        custom_fields = self.view.get_custom_fields(form)
        self.assertEqual(custom_fields, {
            'campaign_id': '',
            'project': 'mozillafoundation',
            'locale': 'en-US',
            'fraud_site_id': 'mofo',
            'landing_url': 'http://localhost',
        })

    def test_get_address_info(self):
        info = self.view.get_address_info(self.form_data)
        self.assertEqual(info, {
            'street_address': self.form_data['address_line_1'],
            'locality': self.form_data['city'],
            'postal_code': self.form_data['post_code'],
            'country_code_alpha2': self.form_data['country'],
        })

    def test_create_customer(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
            self.view.create_customer(form)

        mock_gateway.customer.create.assert_called_once_with({
            'first_name': self.form_data['first_name'],
            'last_name': self.form_data['last_name'],
            'email': self.form_data['email'],
            'payment_method_nonce': 'hello-braintree',
            'custom_fields': {
                'project': 'mozillafoundation',
                'campaign_id': '',
                'locale': 'en-US',
                'fraud_site_id': 'mofo',
                'landing_url': 'http://localhost',
            },
            'credit_card': {
                'billing_address': {
                    'street_address': self.form_data['address_line_1'],
                    'locality': self.form_data['city'],
                    'postal_code': self.form_data['post_code'],
                    'country_code_alpha2': self.form_data['country'],
                }
            },
            'device_data': self.form_data['device_data'],
        })


class SingleCardPaymentViewTestCase(CardPaymentViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.payment_frequency = 'single'

    def test_transaction_data_submitted_to_braintree(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()

        with mock.patch.object(CardPaymentView, 'create_customer', autospec=True) as mock_create_customer:
            mock_create_customer.return_value.is_success = True
            mock_create_customer.return_value.customer = MockBraintreeCustomer()
            with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
                self.view.form_valid(form, send_data_to_basket=False)

        mock_gateway.transaction.sale.assert_called_once_with({
            'merchant_account_id': 'usd-ac',
            'payment_method_token': 'payment-method-1',
            'amount': Decimal(50),
            'options': {
                'submit_for_settlement': True,
            },
            'device_data': '{"some": "data"}',
        })

        self.assertEqual(self.request.session['landing_url'], self.form_data['landing_url'])
        self.assertEqual(self.request.session['campaign_id'], self.form_data['campaign_id'])
        self.assertEqual(self.request.session['project'], self.form_data['project'])

    def test_ga_transaction_and_event(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()

        with mock.patch.object(CardPaymentView, 'create_customer', autospec=True) as mock_create_customer:
            mock_create_customer.return_value.is_success = True
            mock_create_customer.return_value.customer = MockBraintreeCustomer()
            with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
                mock_gateway.transaction.sale.return_value = MockBraintreeResult()
                with mock.patch.object(CardPaymentView, 'queue_ga_transaction') as mock_queue_tx:
                    with mock.patch('donate.payments.views.queue_ga_event') as mock_queue_event:
                        self.view.form_valid(form, send_data_to_basket=False)

        mock_queue_tx.assert_called_once_with(
            id='transaction-id-1',
            currency='usd',
            amount=Decimal(50),
            name='Card Donation',
            category='one-time'
        )
        mock_queue_event.assert_called_once_with(self.view.request, ['send', 'event', {
                'eventCategory': 'Donation',
                'eventAction': 'Card',
                'eventLabel': 'Single',
            }
        ])

    def test_get_success_url(self):
        self.assertEqual(
            self.view.get_success_url(),
            reverse('payments:card_upsell')
        )

    def test_get_transaction_details_for_session(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()
        details = self.view.get_transaction_details_for_session(
            MockBraintreeResult(),
            form,
            payment_method_token='token-1',
            transaction_id='transaction-id-1',
            last_4='5678',
            settlement_amount=Decimal(10),
        )

        expected_details = self.form_data.copy()
        expected_details.update({
            'transaction_id': 'transaction-id-1',
            'payment_method': 'Braintree_Card',
            'payment_frequency': 'single',
            'payment_method_token': 'token-1',
            'currency': 'usd',
            'card_type': 'Visa',
            'last_4': '5678',
            'settlement_amount': Decimal(10),
        })
        self.assertEqual(details, expected_details)

        # Ensure that the details are valid for what the basket task expects
        with mock.patch('donate.payments.tasks.send_to_sqs') as mock_send:
            send_transaction_to_basket(self.view.prepare_session_data(details))
        mock_send.assert_called_once()


class MonthlyCardPaymentViewTestCase(CardPaymentViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.payment_frequency = 'monthly'

    @freeze_time('2019-07-26')
    def test_subscription_data_submitted_to_braintree(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()

        with mock.patch.object(CardPaymentView, 'create_customer', autospec=True) as mock_create_customer:
            mock_create_customer.return_value.is_success = True
            mock_create_customer.return_value.customer = MockBraintreeCustomer()
            with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
                self.view.form_valid(form)

        mock_gateway.subscription.create.assert_called_once_with({
            'plan_id': 'usd-plan',
            'merchant_account_id': 'usd-ac',
            'payment_method_token': 'payment-method-1',
            'price': 50,
            'first_billing_date': date(2019, 7, 26),
        })

        self.assertEqual(self.request.session['landing_url'], self.form_data['landing_url'])
        self.assertEqual(self.request.session['campaign_id'], self.form_data['campaign_id'])
        self.assertEqual(self.request.session['project'], self.form_data['project'])

    def test_ga_transaction_and_event(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()

        with mock.patch.object(CardPaymentView, 'create_customer', autospec=True) as mock_create_customer:
            mock_create_customer.return_value.is_success = True
            mock_create_customer.return_value.customer = MockBraintreeCustomer()
            with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
                mock_gateway.subscription.create.return_value = MockBraintreeSubscriptionResult()
                with mock.patch.object(CardPaymentView, 'queue_ga_transaction') as mock_queue_tx:
                    with mock.patch('donate.payments.views.queue_ga_event') as mock_queue_event:
                        self.view.form_valid(form, send_data_to_basket=False)

        mock_queue_tx.assert_called_once_with(
            id='subscription-id-1',
            currency='usd',
            amount=Decimal(50),
            name='Card Donation',
            category='monthly'
        )
        mock_queue_event.assert_called_once_with(self.view.request, ['send', 'event', {
                'eventCategory': 'Donation',
                'eventAction': 'Card',
                'eventLabel': 'Monthly',
            }
        ])

    def test_failed_customer_creation_calls_error_processor(self):
        form = BraintreeCardPaymentForm(self.form_data)
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
            mock_gateway.customer.create.return_value.is_success = False
            response = self.view.form_valid(form)

        self.assertFalse(form.is_valid())
        self.assertTrue(response.status_code, 200)

    def test_get_success_url(self):
        self.assertEqual(
            self.view.get_success_url(),
            reverse('payments:newsletter_signup')
        )


class PaypalPaymentViewTestCase(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.session = self.client.session
        self.request.LANGUAGE_CODE = 'en-US'
        self.view = PaypalPaymentView()
        self.view.request = self.request
        self.form_data = {
            'braintree_nonce': 'hello-braintree',
            'amount': Decimal(10),
            'currency': 'usd',
            'frequency': 'single',
            'landing_url': 'http://localhost',
            'project': 'mozillafoundation',
            'campaign_id': '',
        }

    def test_transaction_data_submitted_to_braintree(self):
        form = BraintreePaypalPaymentForm(self.form_data)
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
            mock_gateway.transaction.sale.return_value = MockBraintreeResult()
            self.view.form_valid(form, send_data_to_basket=False)

        mock_gateway.transaction.sale.assert_called_once_with({
            'amount': 10,
            'custom_fields': {
                'project': 'mozillafoundation',
                'campaign_id': '',
                'locale': 'en-US',
                'fraud_site_id': 'mofo',
                'landing_url': 'http://localhost'
            },
            'payment_method_nonce': 'hello-braintree',
            'merchant_account_id': 'usd-ac',
            'options': {'submit_for_settlement': True}
        })

        self.assertEqual(self.request.session['landing_url'], self.form_data['landing_url'])
        self.assertEqual(self.request.session['campaign_id'], self.form_data['campaign_id'])
        self.assertEqual(self.request.session['project'], self.form_data['project'])

    def test_ga_transaction(self):
        form = BraintreePaypalPaymentForm(self.form_data)
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
            mock_gateway.transaction.sale.return_value = MockBraintreeResult()
            with mock.patch.object(PaypalPaymentView, 'queue_ga_transaction') as mock_queue_tx:
                with mock.patch('donate.payments.views.queue_ga_event') as mock_queue_event:
                    self.view.form_valid(form, send_data_to_basket=False)

        mock_queue_tx.assert_called_once_with(
            id='transaction-id-1',
            currency='usd',
            amount=Decimal(10),
            name='PayPal Donation',
            category='one-time'
        )
        mock_queue_event.assert_called_once_with(self.view.request, ['send', 'event', {
                'eventCategory': 'Donation',
                'eventAction': 'PayPal',
                'eventLabel': 'Single',
            }
        ])

    @freeze_time('2019-07-26')
    def test_subscription_data_submitted_to_braintree(self):
        self.form_data['frequency'] = 'monthly'
        form = BraintreePaypalPaymentForm(self.form_data)
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
            mock_gateway.customer.create.return_value.is_success = True
            mock_gateway.customer.create.return_value.customer = MockBraintreeCustomer()
            self.view.form_valid(form, send_data_to_basket=False)

        mock_gateway.customer.create.assert_called_once_with({
            'payment_method_nonce': 'hello-braintree',
            'custom_fields': {
                'project': 'mozillafoundation',
                'campaign_id': '',
                'locale': 'en-US',
                'fraud_site_id': 'mofo',
                'landing_url': 'http://localhost',
            },
        })

        mock_gateway.subscription.create.assert_called_once_with({
            'plan_id': 'usd-plan',
            'merchant_account_id': 'usd-ac',
            'payment_method_token': 'payment-method-1',
            'price': Decimal(10),
            'first_billing_date': date(2019, 7, 26),
        })

    def test_failed_customer_creation_calls_form_invalid(self):
        self.form_data['frequency'] = 'monthly'
        form = BraintreePaypalPaymentForm(self.form_data)
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
            mock_gateway.customer.create.return_value.is_success = False
            with mock.patch.object(PaypalPaymentView, 'form_invalid') as mock_form_invalid:
                self.view.form_valid(form)

        mock_form_invalid.assert_called_once()

    def test_get_transaction_details_for_session(self):
        self.form_data['frequency'] = 'monthly'
        form = BraintreePaypalPaymentForm(self.form_data)
        assert form.is_valid()
        self.view.payment_frequency = 'monthly'
        self.view.currency = 'usd'
        result = MockBraintreeSubscriptionResult()
        payment_method = MockBraintreePaymentMethod()
        details = self.view.get_transaction_details_for_session(result, form, payment_method=payment_method)
        self.assertEqual(
            details,
            {
                'amount': Decimal(10),
                'transaction_id': 'subscription-id-1',
                'payment_method': 'Braintree_Paypal',
                'payment_frequency': 'monthly',
                'currency': 'usd',
                'settlement_amount': None,
                'email': 'test@example.com',
                'first_name': 'Bob',
                'last_name': 'Jones',
                'campaign_id': '',
                'project': 'mozillafoundation',
                'landing_url': 'http://localhost',
            }
        )

        # Ensure that the details are valid for what the basket task expects
        with mock.patch('donate.payments.tasks.send_to_sqs') as mock_send:
            send_transaction_to_basket(self.view.prepare_session_data(details))
        mock_send.assert_called_once()

    def test_get_success_url_single(self):
        self.view.payment_frequency = 'single'
        self.assertEqual(
            self.view.get_success_url(),
            reverse('payments:paypal_upsell')
        )

    def test_get_success_url_monthly(self):
        self.view.payment_frequency = 'monthly'
        self.assertEqual(
            self.view.get_success_url(),
            reverse('payments:newsletter_signup')
        )

    def test_form_invalid_redirects_to_referrer(self):
        self.view.request.META['HTTP_REFERER'] = f'http://{self.view.request.get_host()}'
        with mock.patch('donate.payments.views.messages', autospec=True):
            response = self.view.form_invalid(BraintreePaypalPaymentForm())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], f'http://{self.view.request.get_host()}')

    def test_form_invalid_redirects_to_home_if_unsafe_referrer(self):
        self.view.request.META['HTTP_REFERER'] = 'https://example.com'
        with mock.patch('donate.payments.views.messages', autospec=True):
            response = self.view.form_invalid(BraintreePaypalPaymentForm())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')


class TransactionRequiredMixinTestCase(TestCase):

    def test_missing_transaction_redirects(self):
        view = TransactionRequiredMixin()
        view.request = RequestFactory().get('/')
        view.request.session = self.client.session
        response = view.dispatch(view.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')


class CardUpsellViewTestCase(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.LANGUAGE_CODE = 'en-US'
        self.request.session = self.client.session
        self.request.session['completed_transaction_details'] = {
            'first_name': 'Alice',
            'last_name': 'Bob',
            'email': 'alice@example.com',
            'address_line_1': '1 Oak Tree Hill',
            'city': 'New York',
            'post_code': '10022',
            'country': 'US',
            'amount': 50,
            'currency': 'usd',
            'payment_frequency': 'single',
            'payment_method': 'Braintree_Card',
            'payment_method_token': 'payment-method-1',
        }
        self.view = CardUpsellView()
        self.view.request = self.request

    def test_skips_if_previous_transaction_was_not_card(self):
        self.request.session['completed_transaction_details']['payment_method'] = 'Braintree_Paypal'
        response = self.view.dispatch(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('payments:newsletter_signup'))

    def test_skips_if_previous_transaction_was_not_single(self):
        self.request.session['completed_transaction_details']['payment_frequency'] = 'monthly'
        response = self.view.dispatch(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('payments:newsletter_signup'))

    def test_skips_if_previous_transaction_was_too_small(self):
        self.request.session['completed_transaction_details']['amount'] = 1
        response = self.view.dispatch(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('payments:newsletter_signup'))

    @freeze_time('2019-07-26')
    def test_subscription_data_submitted_to_braintree(self):
        form = UpsellForm({'amount': Decimal(15), 'currency': 'usd'}, initial={'currency': 'usd'})
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
            self.view.form_valid(form)

        mock_gateway.subscription.create.assert_called_once_with({
            'plan_id': 'usd-plan',
            'merchant_account_id': 'usd-ac',
            'payment_method_token': 'payment-method-1',
            'price': Decimal(15),
            'first_billing_date': FakeDate(2019, 8, 26),
        })

    def test_ga_transaction(self):
        form = UpsellForm({'amount': Decimal(15), 'currency': 'usd'}, initial={'currency': 'usd'})
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
            mock_gateway.subscription.create.return_value = MockBraintreeSubscriptionResult()
            with mock.patch.object(CardUpsellView, 'queue_ga_transaction') as mock_queue_tx:
                self.view.form_valid(form)

        mock_queue_tx.assert_called_once_with(
            id='subscription-id-1',
            currency='usd',
            amount=Decimal(15),
            name='Card Donation',
            category='monthly'
        )

    def test_failed_customer_creation_calls_error_processor(self):
        form = UpsellForm({'amount': Decimal(15), 'currency': 'usd'}, initial={'currency': 'usd'})
        assert form.is_valid()
        self.view.currency = 'usd'

        with mock.patch('donate.payments.views.gateway', autospec=True) as mock_gateway:
            mock_gateway.subscription.create.return_value.is_success = False
            response = self.view.form_valid(form)

        self.assertFalse(form.is_valid())
        self.assertTrue(response.status_code, 200)

    def test_get_transaction_details_for_session(self):
        form = UpsellForm({'amount': Decimal(17), 'currency': 'usd'}, initial={'currency': 'usd'})
        assert form.is_valid()

        mock_result = MockBraintreeSubscriptionResult()
        self.assertEqual(
            self.view.get_transaction_details_for_session(mock_result, form, currency='usd'),
            {
                'amount': Decimal(17),
                'transaction_id': 'subscription-id-1',
                'payment_method': 'Braintree_Card',
                'currency': 'usd',
                'payment_frequency': 'monthly',
                'country': 'US',
                'first_name': 'Alice',
                'last_name': 'Bob',
                'email': 'alice@example.com',
                'payment_method_token': 'payment-method-1',
                'address_line_1': '1 Oak Tree Hill',
                'post_code': '10022',
                'city': 'New York',
            }
        )


class PaypalUpsellViewTestCase(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.session = self.client.session
        self.request.session['completed_transaction_details'] = {
            'amount': 50,
            'currency': 'usd',
            'payment_frequency': 'single',
            'payment_method': 'Braintree_Paypal',
            'payment_method_token': 'payment-method-1',
        }
        self.request.LANGUAGE_CODE = 'en-US'
        self.view = PaypalUpsellView()
        self.view.request = self.request

    def test_skips_if_previous_transaction_was_not_paypal(self):
        self.request.session['completed_transaction_details']['payment_method'] = 'Braintree_Card'
        response = self.view.dispatch(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('payments:newsletter_signup'))

    def test_skips_if_previous_transaction_was_not_single(self):
        self.request.session['completed_transaction_details']['payment_frequency'] = 'monthly'
        response = self.view.dispatch(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('payments:newsletter_signup'))

    def test_skips_if_previous_transaction_was_too_small(self):
        self.request.session['completed_transaction_details']['amount'] = 1
        response = self.view.dispatch(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('payments:newsletter_signup'))

    @freeze_time('2019-07-26')
    def test_subscription_data_submitted_to_braintree(self):
        form = BraintreePaypalUpsellForm({
            'amount': Decimal(15), 'braintree_nonce': 'hello-braintree', 'currency': 'usd'
        }, initial={'currency': 'usd'})
        assert form.is_valid()
        self.view.currency = 'usd'

        with mock.patch('donate.payments.views.gateway') as mock_gateway:
            mock_gateway.customer.create.return_value.is_success = True
            mock_gateway.customer.create.return_value.customer = MockBraintreeCustomer()
            self.view.form_valid(form)

        mock_gateway.subscription.create.assert_called_once_with({
            'plan_id': 'usd-plan',
            'merchant_account_id': 'usd-ac',
            'payment_method_token': 'payment-method-1',
            'price': Decimal(15),
            'first_billing_date': FakeDate(2019, 8, 26)
        })

    def test_ga_transaction(self):
        form = BraintreePaypalUpsellForm({
            'amount': Decimal(15),
            'braintree_nonce': 'hello-braintree',
            'currency': 'usd'
        }, initial={'currency': 'usd'})
        assert form.is_valid()

        with mock.patch('donate.payments.views.gateway') as mock_gateway:
            mock_gateway.customer.create.return_value.is_success = True
            mock_gateway.customer.create.return_value.customer = MockBraintreeCustomer()
            mock_gateway.subscription.create.return_value = MockBraintreeSubscriptionResult()
            with mock.patch.object(PaypalUpsellView, 'queue_ga_transaction') as mock_queue_tx:
                self.view.form_valid(form)

        mock_queue_tx.assert_called_once_with(
            id='subscription-id-1',
            currency='usd',
            amount=Decimal(15),
            name='PayPal Donation',
            category='monthly'
        )

    def test_failed_customer_creation_calls_error_processor(self):
        form = BraintreePaypalUpsellForm({
            'amount': Decimal(15), 'braintree_nonce': 'hello-braintree', 'currency': 'usd'
        }, initial={'currency': 'usd'})
        assert form.is_valid()
        self.view.currency = 'usd'

        with mock.patch('donate.payments.views.gateway') as mock_gateway:
            mock_gateway.subscription.create.return_value.is_success = False
            response = self.view.form_valid(form)

        self.assertFalse(form.is_valid())
        self.assertTrue(response.status_code, 200)

    def test_get_transaction_details_for_session(self):
        form = BraintreePaypalUpsellForm({
            'amount': Decimal(17), 'braintree_nonce': 'hello-braintree', 'currency': 'usd'
        }, initial={'currency': 'usd'})
        assert form.is_valid()

        self.view.currency = 'usd'
        self.view.payment_frequency = 'monthly'
        mock_result = MockBraintreeSubscriptionResult()
        self.assertEqual(
            self.view.get_transaction_details_for_session(mock_result, form, currency='usd'),
            {
                'amount': Decimal(17),
                'transaction_id': 'subscription-id-1',
                'braintree_nonce': 'hello-braintree',
                'payment_method': 'Braintree_Paypal',
                'currency': 'usd',
                'payment_frequency': 'monthly',
                'payment_method_token': 'payment-method-1',
            }
        )


class NewsletterSignupViewTestCase(TestCase):

    def test_skips_if_subscribed(self):
        request = RequestFactory().get('/')
        request.COOKIES['subscribed'] = '1'
        view = NewsletterSignupView()
        response = view.get(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], view.get_success_url())

    def test_get_initial_populates_email_from_session(self):
        request = RequestFactory().get('/')
        request.session = {
            'completed_transaction_details': {
                'email': 'test@example.com',
            }
        }
        view = NewsletterSignupView()
        view.request = request
        self.assertEqual(view.get_initial(), {
            'email': 'test@example.com',
        })
