from decimal import Decimal
import json
from unittest import mock

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase, override_settings

from freezegun import freeze_time

from ..tasks import send_newsletter_subscription_to_basket, send_transaction_to_basket


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
            'payment_method': 'card',
            'transaction_id': 'transaction-1',
            'landing_url': 'http://localhost',
            'project': 'mozillafoundation',
            'last_4': '1234',
            'locale': 'en-US',
            'settlement_amount': Decimal(10),
        }

        self.sample_payload = {
            'event_type': 'donation',
            'last_name': 'Bob',
            'email': 'test@example.com',
            'donation_amount': Decimal(10),
            'currency': 'usd',
            'created': 1565222400,
            'recurring': False,
            'service': 'card',
            'transaction_id': 'transaction-1',
            'project': 'mozillafoundation',
            'last_4': '1234',
            'donation_url': 'http://localhost',
            'locale': 'en-US',
            'conversion_amount': Decimal(10),
        }

    def test_sqs_payload(self):
        with mock.patch('donate.payments.tasks.sqs_client', autospec=True) as mock_client:
            send_transaction_to_basket(self.sample_data)
        expected_json = json.dumps(self.sample_payload, cls=DjangoJSONEncoder, sort_keys=True)
        mock_client.return_value.send_message.assert_called_once_with(
            QueueUrl=settings.BASKET_SQS_QUEUE_URL,
            MessageBody=expected_json,
        )

    def test_send_transaction_to_basket_single(self):
        self.test_sqs_payload()

    def test_send_transaction_to_basket_monthly(self):
        self.sample_data['payment_frequency'] = 'monthly'
        self.sample_data['settlement_amount'] = None
        self.sample_payload['recurring'] = True
        self.sample_payload['conversion_amount'] = None
        self.test_sqs_payload()
