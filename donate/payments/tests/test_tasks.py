from decimal import Decimal
from unittest import mock

from django.test import TestCase, override_settings

from freezegun import freeze_time

from ..tasks import (
    BraintreeWebhookProcessor, send_newsletter_subscription_to_basket, send_transaction_to_basket
)


class NewsletterSignupTestCase(TestCase):

    def test_newsletter_signup_request_to_basket(self):
        with mock.patch('donate.payments.tasks.requests', autospec=True) as mock_requests:
            send_newsletter_subscription_to_basket({
                'lang': 'en',
                'source_url': 'http://localhost/donate/thanks/',
                'email': 'test@example.com'
            })
        mock_requests.post.assert_called_once_with('http://localhost/news/subscribe', json={
            'format': 'html',
            'lang': 'en',
            'newsletters': 'mozilla-foundation',
            'trigger_welcome': 'N',
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
            'last_name': 'Bob',
            'email': 'test@example.com',
            'amount': Decimal(10),
            'currency': 'usd',
            'payment_frequency': 'single',
            'payment_method': 'Braintree_Card',
            'transaction_id': 'transaction-1',
            'landing_url': 'http://localhost',
            'project': 'mozillafoundation',
            'last_4': '1234',
            'locale': 'en-US',
            'settlement_amount': Decimal(10),
        }

        self.sample_payload = {
            'data': {
                'event_type': 'donation',
                'last_name': 'Bob',
                'email': 'test@example.com',
                'donation_amount': Decimal(10),
                'currency': 'usd',
                'created': 1565222400,
                'recurring': False,
                'service': 'Braintree_Card',
                'transaction_id': 'transaction-1',
                'project': 'mozillafoundation',
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
        self.sample_payload['data']['recurring'] = True
        self.sample_payload['data']['conversion_amount'] = None
        self._test_sqs_payload()


class ProcessWebhookTestCase(TestCase):

    def test_processor_calls_method_based_on_kind(self):
        notification = mock.Mock()
        notification.kind = 'subscription_charged_unsuccessfully'
        with mock.patch.object(
            BraintreeWebhookProcessor, 'process_subscription_charged_unsuccessfully'
        ) as mock_process_method:
            BraintreeWebhookProcessor().process(notification)

        mock_process_method.assert_called_once_with(notification)

    def test_process_subscription_charged_unsuccessfully(self):
        notification = mock.Mock()
        notification.kind = 'subscription_charged_unsuccessfully'
        notification.subscription.id = 'test-id'
        tx = mock.Mock()
        tx.status = 'failed'
        notification.subscription.transactions = [tx]

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            BraintreeWebhookProcessor().process_subscription_charged_unsuccessfully(notification)
        mock_send.assert_called_once_with({
            'data': {
                'event_type': 'charge.failed',
                'transaction_id': 'test-id',
                'failure_code': 'failed',
            }
        })

    def test_process_dispute_lost(self):
        notification = mock.Mock()
        notification.kind = 'dispute_lost'
        notification.dispute.transaction.id = 'test-id'
        notification.dispute.reason = 'fraud'

        with mock.patch('donate.payments.tasks.send_to_sqs', autospec=True) as mock_send:
            BraintreeWebhookProcessor().process_dispute_lost(notification)
        mock_send.assert_called_once_with({
            'data': {
                'event_type': 'charge.dispute.closed',
                'status': 'lost',
                'transaction_id': 'test-id',
                'failure_code': 'fraud',
            }
        })
