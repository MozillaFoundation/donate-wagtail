from unittest import mock

from django.test import TestCase

from ..braintree_webhooks import WebhookForm, BraintreeWebhookView
from ..tasks import process_webhook


class BraintreeWebhookViewTestCase(TestCase):

    def test_form_valid_queues_task(self):
        form = WebhookForm({
            'bt_signature': 'signature',
            'bt_payload': 'payload'
        })
        assert form.is_valid()
        with mock.patch('donate.payments.braintree_webhooks.queue') as mock_queue:
            response = BraintreeWebhookView().form_valid(form)

        mock_queue.enqueue.assert_called_once_with(
            process_webhook, form.cleaned_data,
            description="Handle Braintree webhook"
        )
        self.assertEqual(response.status_code, 200)

    def test_form_invalid_returns_400(self):
        form = WebhookForm({})
        response = BraintreeWebhookView().form_invalid(form)
        self.assertEqual(response.status_code, 400)
