from decimal import Decimal
from unittest import mock
import stripe

from django.test import TestCase, override_settings

from freezegun import freeze_time

from ..tasks import (
    BraintreeWebhookProcessor, send_newsletter_subscription_to_basket, send_transaction_to_basket,
    StripeWebhookProcessor)


class NewsletterSignupTestCase(TestCase):

    def test_newsletter_signup_request_to_basket(self):
        with mock.patch('donate.payments.tasks.requests', autospec=True) as mock_requests:
            send_newsletter_subscription_to_basket({
                'lang': 'en',
                'source_url': 'http://localhost/donate/thanks/',
                'email': 'test@example.com'
            })
        mock_requests.post.assert_called_once_with('http://localhost/news/subscribe/', data={
            'format': 'html',
            'lang': 'en',
            'newsletters': 'mozilla-foundation',
            'source_url': 'http://localhost/donate/thanks/',
            'email': 'test@example.com',
        })

    @override_settings(BASKET_API_ROOT_URL=None)
    def test_newsletter_signup_does_nothing_if_no_api_url_set(self):
        with mock.patch('donate.payments.tasks.requests', autospec=True) as mock_requests:
            result = send_newsletter_subscription_to_basket({
                'lang': 'en',
                'source_url': 'http://localhost/donate/thanks/',
                'email': 'test@example.com'
            })
        mock_requests.post.assert_not_called()
        self.assertIsNone(result)


@freeze_time("2019-08-08 00:00:00", tz_offset=0)
class BasketTransactionTestCase(TestCase):

    def setUp(self):
        self.sample_data = {
            'last_name': 'Bobbertson',
            'first_name': 'Bob',
            'campaign_id': '',
            'email': 'test@example.com',
            'amount': Decimal(10),
            'currency': 'usd',
            'payment_frequency': 'single',
            'payment_method': 'Braintree_Card',
            'transaction_id': 'transaction-1',
            'landing_url': 'http://localhost',
            'project': 'mozillafoundation',
            'card_type': 'Visa',
            'last_4': '1234',
            'locale': 'en-US',
            'settlement_amount': Decimal(10),
        }

        self.sample_payload = {
            'data': {
                'event_type': 'donation',
                'last_name': 'Bobbertson',
                'first_name': 'Bob',
                'campaign_id': '',
                'email': 'test@example.com',
                'donation_amount': Decimal(10),
                'currency': 'usd',
                'created': 1565222400,
                'recurring': False,
                'service': 'Braintree_Card',
                'transaction_id': 'transaction-1',
                'subscription_id': None,
                'project': 'mozillafoundation',
                'card_type': 'Visa',
                'last_4': '1234',
                'donation_url': 'http://localhost',
                'locale': 'en-US',
                'conversion_amount': Decimal(10),
            }
        }

    def _test_sqs_payload(self):
        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            send_transaction_to_basket(self.sample_data)
        mock_send.assert_called_once_with(self.sample_payload)

    def test_send_transaction_to_basket_single(self):
        self._test_sqs_payload()

    def test_send_transaction_to_basket_monthly(self):
        self.sample_data['payment_frequency'] = 'monthly'
        self.sample_data['settlement_amount'] = None
        self.sample_data['subscription_id'] = 'test-subscription-id'
        self.sample_payload['data']['recurring'] = True
        self.sample_payload['data']['conversion_amount'] = None
        self.sample_payload['data']['subscription_id'] = 'test-subscription-id'
        self._test_sqs_payload()


class ProcessWebhookTestCase(TestCase):

    def test_processor_calls_method_based_on_kind(self):
        notification = mock.Mock()
        notification.kind = 'subscription_charged_unsuccessfully'
        with mock.patch.object(
            BraintreeWebhookProcessor, 'subscription_charged_unsuccessfully'
        ) as mock_process_method:
            BraintreeWebhookProcessor().process(notification)

        mock_process_method.assert_called_once_with(notification)

    @freeze_time("2019-08-08 00:00:00", tz_offset=0)
    def test_subscription_charged_successfully_credit(self):
        notification = mock.Mock()
        notification.kind = 'subscription_charged_successfully'
        tx = mock.Mock()
        tx.id = 'test-id'
        tx.customer_details = mock.Mock()
        tx.customer_details.first_name = 'Bob'
        tx.customer_details.last_name = 'Geldof'
        tx.customer_details.email = 'test@example.com'
        tx.amount = Decimal(10)
        tx.currency_iso_code = 'USD'
        tx.payment_instrument_type = 'credit_card'
        tx.credit_card_details = mock.Mock()
        tx.credit_card_details.card_type = 'Visa'
        tx.credit_card_details.last_4 = '1234'
        tx.disbursement_details = mock.Mock()
        tx.disbursement_details.settlement_amount = Decimal(10)
        notification.subscription.transactions = [tx]
        notification.subscription.id = 'test-subscription-id'

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            with mock.patch('donate.payments.tasks.gateway', autospec=True) as mock_gateway:
                mock_payment_method = mock.Mock()
                mock_payment_method.customer_id = 'customer-1'
                mock_gateway.payment_method.find.return_value = mock_payment_method
                mock_customer = mock.Mock()
                mock_customer.custom_fields = {
                    'campaign_id': 'PIDAY',
                    'project': 'mozillafoundation',
                    'locale': 'en-US',
                }
                mock_gateway.customer.find.return_value = mock_customer
                BraintreeWebhookProcessor().subscription_charged_successfully(notification)
        mock_send.assert_called_once_with({
            'data': {
                'event_type': 'donation',
                'last_name': 'Geldof',
                'first_name': 'Bob',
                'campaign_id': 'PIDAY',
                'email': 'test@example.com',
                'donation_amount': Decimal(10),
                'currency': 'usd',
                'created': 1565222400,
                'recurring': True,
                'service': 'Braintree_Card',
                'transaction_id': 'test-id',
                'subscription_id': 'test-subscription-id',
                'project': 'mozillafoundation',
                'card_type': 'Visa',
                'last_4': '1234',
                'donation_url': '',
                'locale': 'en-US',
                'conversion_amount': Decimal(10),
            }
        })

    @freeze_time("2019-08-08 00:00:00", tz_offset=0)
    def test_subscription_without_project_update_fail(self):
        notification = mock.Mock()
        notification.kind = 'subscription_charged_successfully'
        tx = mock.Mock()
        tx.id = 'test-id'
        tx.customer_details = mock.Mock()
        tx.customer_details.first_name = 'Bob'
        tx.customer_details.last_name = 'Geldof'
        tx.customer_details.email = 'test@example.com'
        tx.amount = Decimal(10)
        tx.currency_iso_code = 'USD'
        tx.payment_instrument_type = 'credit_card'
        tx.credit_card_details = mock.Mock()
        tx.credit_card_details.card_type = 'Visa'
        tx.credit_card_details.last_4 = '1234'
        tx.disbursement_details = mock.Mock()
        tx.disbursement_details.settlement_amount = Decimal(10)
        notification.subscription.transactions = [tx]
        notification.subscription.id = 'test-subscription-id'

        with mock.patch('donate.payments.tasks.logger') as mock_logger:
            with mock.patch('donate.payments.tasks.gateway', autospec=True) as mock_gateway:
                mock_payment_method = mock.Mock()
                mock_payment_method.customer_id = 'customer-1'
                mock_gateway.payment_method.find.return_value = mock_payment_method
                mock_customer = mock.Mock()
                mock_customer.id = 'test-customer-id'
                mock_customer.custom_fields = {
                    'campaign_id': 'PIDAY',
                    'locale': 'en-US',
                }
                mock_gateway.customer.find.return_value = mock_customer
                mock_gateway.customer.update.return_value = DotDict({
                  'is_success': False
                })
                BraintreeWebhookProcessor().subscription_charged_successfully(notification)

        mock_logger.error.assert_called_once()

    @freeze_time("2019-08-08 00:00:00", tz_offset=0)
    def test_subscription_without_project(self):
        notification = mock.Mock()
        notification.kind = 'subscription_charged_successfully'
        tx = mock.Mock()
        tx.id = 'test-id'
        tx.customer_details = mock.Mock()
        tx.customer_details.first_name = 'Bob'
        tx.customer_details.last_name = 'Geldof'
        tx.customer_details.email = 'test@example.com'
        tx.amount = Decimal(10)
        tx.currency_iso_code = 'USD'
        tx.payment_instrument_type = 'credit_card'
        tx.credit_card_details = mock.Mock()
        tx.credit_card_details.card_type = 'Visa'
        tx.credit_card_details.last_4 = '1234'
        tx.disbursement_details = mock.Mock()
        tx.disbursement_details.settlement_amount = Decimal(10)
        notification.subscription.transactions = [tx]
        notification.subscription.id = 'test-subscription-id'

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send: # noqa
            with mock.patch('donate.payments.tasks.gateway', autospec=True) as mock_gateway:
                mock_payment_method = mock.Mock()
                mock_payment_method.customer_id = 'customer-1'
                mock_gateway.payment_method.find.return_value = mock_payment_method
                mock_customer = mock.Mock()
                mock_customer.id = 'test-customer-id'
                mock_customer.custom_fields = {
                    'campaign_id': 'PIDAY',
                    'locale': 'en-US',
                }
                mock_gateway.customer.find.return_value = mock_customer
                BraintreeWebhookProcessor().subscription_charged_successfully(notification)

        mock_gateway.customer.update.assert_called_once_with('test-customer-id', {
            'custom_fields': {
                'campaign_id': 'PIDAY',
                'locale': 'en-US',
                'project': 'mozillafoundation'
            }
        })

    @freeze_time("2019-08-08 00:00:00", tz_offset=0)
    def test_process_credit_subscription_charged_successfully_paypal(self):
        notification = mock.Mock()
        notification.kind = 'subscription_charged_successfully'
        tx = mock.Mock()
        tx.id = 'test-id'
        tx.paypal_details = mock.Mock()
        tx.paypal_details.payer_first_name = 'Bob'
        tx.paypal_details.payer_last_name = 'Geldof'
        tx.paypal_details.payer_email = 'test@example.com'
        tx.amount = Decimal(10)
        tx.currency_iso_code = 'USD'
        tx.payment_instrument_type = 'paypal_account'
        tx.disbursement_details = mock.Mock()
        tx.disbursement_details.settlement_amount = Decimal(10)
        notification.subscription.transactions = [tx]
        notification.subscription.id = 'test-subscription-id'

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            with mock.patch('donate.payments.tasks.gateway', autospec=True) as mock_gateway:
                mock_payment_method = mock.Mock()
                mock_payment_method.customer_id = 'customer-1'
                mock_gateway.payment_method.find.return_value = mock_payment_method
                mock_customer = mock.Mock()
                mock_customer.custom_fields = {
                    'campaign_id': 'PIDAY',
                    'project': 'mozillafoundation',
                    'locale': 'en-US',
                }
                mock_gateway.customer.find.return_value = mock_customer
                BraintreeWebhookProcessor().subscription_charged_successfully(notification)
        mock_send.assert_called_once_with({
            'data': {
                'event_type': 'donation',
                'last_name': 'Geldof',
                'first_name': 'Bob',
                'campaign_id': 'PIDAY',
                'email': 'test@example.com',
                'donation_amount': Decimal(10),
                'currency': 'usd',
                'created': 1565222400,
                'recurring': True,
                'service': 'Braintree_Paypal',
                'transaction_id': 'test-id',
                'subscription_id': 'test-subscription-id',
                'project': 'mozillafoundation',
                'card_type': 'Unknown',
                'last_4': None,
                'donation_url': '',
                'locale': 'en-US',
                'conversion_amount': Decimal(10),
            }
        })

    def test_subscription_charged_unsuccessfully(self):
        notification = mock.Mock()
        notification.kind = 'subscription_charged_unsuccessfully'
        notification.subscription.id = 'test-id'
        tx = mock.Mock()
        tx.status = 'failed'
        notification.subscription.transactions = [tx]

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            BraintreeWebhookProcessor().subscription_charged_unsuccessfully(notification)
        mock_send.assert_called_once_with({
            'data': {
                'event_type': 'charge.failed',
                'transaction_id': 'test-id',
                'failure_code': 'failed',
            }
        })

    def test_dispute_lost(self):
        notification = mock.Mock()
        notification.kind = 'dispute_lost'
        notification.dispute.transaction.id = 'test-id'
        notification.dispute.reason = 'fraud'

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            BraintreeWebhookProcessor().dispute_lost(notification)
        mock_send.assert_called_once_with({
            'data': {
                'event_type': 'charge.dispute.closed',
                'status': 'lost',
                'transaction_id': 'test-id',
                'failure_code': 'fraud',
            }
        })


class DotDict(dict):
    # Stripe uses a class internally that allows for dot notation references to dictionary attributes.
    # To allow this to work in our mocks, this little helper method does the same trick
    def __getattr__(self, attr):
        return self.get(attr)


class ProcessStripeWebhookTestCase(TestCase):

    def get_mock_event(self, type='charge.succeeded'):
        mock_event = mock.Mock()
        mock_event.type = type
        mock_event.data.object.id = 'test-charge-id'
        return mock_event

    def get_mock_charge(self, failure_code=None):
        mock_charge = mock.Mock()
        mock_charge.id = 'test-charge-id'
        mock_charge.amount = 10.00
        mock_charge.currency = 'usd'
        mock_charge.created = 1574801715
        mock_charge.balance_transaction.amount = 1000
        mock_charge.balance_transaction.net = 950
        mock_charge.balance_transaction.fee = 50
        mock_charge.invoice.subscription = 'test-subscription-id'

        if failure_code:
            mock_charge.failure_code = failure_code

        return mock_charge

    def get_mock_subscription(self):
        email = 'donor@example.com'
        mock_subscription = mock.Mock()
        mock_subscription.id = 'test-subscription-id'
        mock_subscription.metadata = DotDict(
            email=email,
            locale='en-US',
            donation_url='donate.mozilla.org'
        )
        mock_subscription.customer.sources.data = [dict(name='Firstname Lastname', last4='4242')]
        mock_subscription.customer.email = email
        return mock_subscription

    def get_mock_invoice(self):
        mock_invoice = mock.Mock()
        mock_invoice.subscription = self.get_mock_subscription()
        return mock_invoice

    def get_mock_dispute_event(self, type, status='needs_response'):
        mock_event = self.get_mock_event(type=type)
        mock_dispute = mock.Mock()
        mock_dispute.id = 'test-dispute-id'
        mock_dispute.charge = 'test-dispute-id'
        mock_dispute.reason = 'fraudulent'
        mock_dispute.status = status
        mock_event.data.object = mock_dispute

        return mock_event

    def test_processor_calls_method_based_on_kind(self):
        event = self.get_mock_event()

        with mock.patch.object(
                StripeWebhookProcessor, 'process_charge_succeeded'
        ) as mock_process_method:
            StripeWebhookProcessor().process(event)

        mock_process_method.assert_called_once_with(event)

    def test_processor_does_not_call_method(self):
        event = self.get_mock_event('charge.failed')

        with mock.patch.object(
                StripeWebhookProcessor, 'process_charge_succeeded'
        ) as mock_process_method:
            StripeWebhookProcessor().process(event)

        mock_process_method.assert_not_called()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_process_charge_succeeded(self):
        mock_event = self.get_mock_event()
        mock_charge = self.get_mock_charge()
        mock_subscription = self.get_mock_subscription()

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
                mock_stripe.Charge.retrieve.return_value = mock_charge
                mock_stripe.Charge.modify = mock.Mock()
                mock_stripe.Subscription.retrieve.return_value = mock_subscription
                mock_stripe.error.StripeError = stripe.error.StripeError
                StripeWebhookProcessor().process_charge_succeeded(mock_event)
            mock_send.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_retrieve_failed(self):
        mock_event = self.get_mock_event()

        with mock.patch('donate.payments.tasks.logger') as mock_logger:
            with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
                mock_stripe.Charge.retrieve.side_effect = stripe.error.StripeError
                mock_stripe.error.StripeError = stripe.error.StripeError
                StripeWebhookProcessor().process_charge_succeeded(mock_event)
            mock_logger.error.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_no_invoice(self):
        mock_event = self.get_mock_event()
        mock_charge = self.get_mock_charge()

        # Have the invoice attribute on the mock charge return no value
        mock_charge.invoice = None

        with mock.patch('donate.payments.tasks.logger') as mock_logger:
            with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
                mock_stripe.Charge.retrieve.return_value = mock_charge
                mock_stripe.error.StripeError = stripe.error.StripeError
                StripeWebhookProcessor().process_charge_succeeded(mock_event)
            mock_logger.info.assert_called_once_with('This charge is not associated with a subscription')

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_no_invoice_subscription(self):
        mock_event = self.get_mock_event()
        mock_charge = self.get_mock_charge()

        # Have the invoice.subscription on the mock charge return no value
        mock_charge.invoice.subscription = None

        with mock.patch('donate.payments.tasks.logger') as mock_logger:
            with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
                mock_stripe.Charge.retrieve.return_value = mock_charge
                mock_stripe.error.StripeError = stripe.error.StripeError
                StripeWebhookProcessor().process_charge_succeeded(mock_event)
            mock_logger.info.assert_called_once_with('This charge is not associated with a subscription')

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_subscription_retrieve_failed(self):
        mock_event = self.get_mock_event()
        mock_charge = self.get_mock_charge()

        with mock.patch('donate.payments.tasks.logger', autospec=True) as mock_logger:
            with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
                mock_stripe.Charge.retrieve.return_value = mock_charge
                mock_stripe.Charge.modify = mock.Mock()
                mock_stripe.Subscription.retrieve.side_effect = stripe.error.StripeError
                mock_stripe.error.StripeError = stripe.error.StripeError
                StripeWebhookProcessor().process_charge_succeeded(mock_event)
            mock_logger.error.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_modify_failed(self):
        mock_event = self.get_mock_event()
        mock_charge = self.get_mock_charge()
        mock_subscription = self.get_mock_subscription()

        with mock.patch('donate.payments.tasks.logger', autospec=True) as mock_logger:
            with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
                mock_stripe.Charge.retrieve.return_value = mock_charge
                mock_stripe.Subscription.retrieve.return_value = mock_subscription
                mock_stripe.Charge.modify = mock.Mock()
                mock_stripe.Charge.modify.side_effect = stripe.error.StripeError
                mock_stripe.error.StripeError = stripe.error.StripeError
                StripeWebhookProcessor().process_charge_succeeded(mock_event)
            mock_logger.error.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_dispute_closed_succeeded(self):
        mock_dispute = self.get_mock_dispute_event('dispute.closed')

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            StripeWebhookProcessor().process_charge_dispute_closed(mock_dispute)
            mock_send.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_dispute_updated_succeeded(self):
        mock_dispute = self.get_mock_dispute_event('dispute.updatedY')

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            StripeWebhookProcessor().process_charge_dispute_updated(mock_dispute)
            mock_send.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_dispute_created_no_auto_close_succeeded(self):
        mock_dispute = self.get_mock_dispute_event('dispute.created')

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            StripeWebhookProcessor().process_charge_dispute_created(mock_dispute)
            mock_send.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    @override_settings(AUTO_CLOSE_STRIPE_DISPUTES=True)
    def test_charge_dispute_created_auto_closed(self):
        mock_dispute = self.get_mock_dispute_event('dispute.created')

        with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
            with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
                StripeWebhookProcessor().process_charge_dispute_created(mock_dispute)
                mock_stripe.Dispute.close.assert_called_once()
                mock_send.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    @override_settings(AUTO_CLOSE_STRIPE_DISPUTES=True)
    def test_charge_dispute_created_auto_close_skipped_if_lost(self):
        mock_dispute = self.get_mock_dispute_event('dispute.created', status='lost')

        with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
            with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
                StripeWebhookProcessor().process_charge_dispute_created(mock_dispute)
                mock_stripe.Dispute.close.assert_not_called()
                mock_send.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    @override_settings(AUTO_CLOSE_STRIPE_DISPUTES=True)
    def test_charge_dispute_created_auto_close_fails(self):
        mock_dispute = self.get_mock_dispute_event('dispute.created')

        with mock.patch('donate.payments.tasks.logger') as mock_logger:
            with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
                mock_stripe.Dispute.close.side_effect = stripe.error.StripeError
                mock_stripe.error.StripeError = stripe.error.StripeError
                with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
                    StripeWebhookProcessor().process_charge_dispute_created(mock_dispute)
                    mock_stripe.Dispute.close.assert_called_once()
                    mock_send.assert_called_once()
                mock_logger.error.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_refunded(self):
        mock_event = self.get_mock_event(type='charge.refunded')
        mock_charge = self.get_mock_charge()
        mock_charge.refunds.data = [DotDict(reason='duplicate', status='succeeded')]
        mock_event.data.object = mock_charge

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            StripeWebhookProcessor().process_charge_refunded(mock_event)
            mock_send.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_refunded_no_reason(self):
        mock_event = self.get_mock_event(type='charge.refunded')
        mock_charge = self.get_mock_charge()
        mock_charge.refunds.data = [DotDict(reason=None, status='succeeded')]
        mock_event.data.object = mock_charge

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            StripeWebhookProcessor().process_charge_refunded(mock_event)
            mock_send.assert_called_once_with({
                'data': {
                    'event_type': 'charge.refunded',
                    'transaction_id': 'test-charge-id',
                    'reason': 'requested_by_customer',
                    'status': 'succeeded'
                }
            })

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_failed(self):
        mock_event = self.get_mock_event(type='charge.failed')
        mock_charge = self.get_mock_charge(failure_code='processing_error')
        mock_charge.invoice = 'test-invoice-id'
        mock_invoice = self.get_mock_invoice()
        mock_event.data.object = mock_charge

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
                mock_stripe.Invoice.retrieve.return_value = mock_invoice
                StripeWebhookProcessor().process_charge_failed(mock_event)
            mock_send.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_failed_no_invoice(self):
        mock_event = self.get_mock_event(type='charge.failed')
        mock_charge = self.get_mock_charge(failure_code='processing_error')
        mock_charge.invoice = None
        mock_event.data.object = mock_charge

        with mock.patch('donate.payments.tasks.logger', autospec=True) as mock_logger:
            with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
                StripeWebhookProcessor().process_charge_failed(mock_event)
                mock_send.assert_not_called()
            mock_logger.info.assert_called_once()

    @freeze_time('2019-11-26 00:00:00', tz_offset=0)
    def test_charge_failed_error_fetching_invoice(self):
        mock_event = self.get_mock_event(type='charge.failed')
        mock_charge = self.get_mock_charge(failure_code='processing_error')
        mock_charge.invoice = 'test-invoice-id'
        mock_event.data.object = mock_charge

        with mock.patch('donate.payments.tasks.logger', autospec=True) as mock_logger:
            with mock.patch('donate.payments.tasks.stripe', autospec=True) as mock_stripe:
                mock_stripe.Invoice.retrieve.side_effect = stripe.error.StripeError
                mock_stripe.error.StripeError = stripe.error.StripeError
                with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
                    StripeWebhookProcessor().process_charge_failed(mock_event)
                    mock_send.assert_not_called()
                mock_stripe.Invoice.retrieve.assert_called_once()
            mock_logger.error.assert_called_once()
