import logging
import time

from django.conf import settings

import django_rq
import requests

from . import constants, gateway
from .sqs import send_to_sqs


logger = logging.getLogger(__name__)

queue = django_rq.get_queue('default')

BASKET_NEWSLETTER_API_PATH = '/news/subscribe/'


def send_newsletter_subscription_to_basket(data):
    if settings.BASKET_API_ROOT_URL is None:
        return

    url = f'{settings.BASKET_API_ROOT_URL}{BASKET_NEWSLETTER_API_PATH}'
    payload = {
        'format': 'html',
        'lang': data['lang'],
        'newsletters': 'mozilla-foundation',
        'source_url': data['source_url'],
        'email': data['email']
    }
    try:
        return requests.post(url, data=payload)
    except requests.exceptions.RequestException:
        logger.exception('Failed to post to basket newsletter API')


def send_transaction_to_basket(data):
    send_to_sqs({
        'data': {
            'event_type': 'donation',
            'last_name': data['last_name'],
            'first_name': data['first_name'],
            'campaign_id': data['campaign_id'],
            'email': data['email'],
            'donation_amount': data['amount'],
            'currency': data['currency'],
            'created': int(time.time()),
            'recurring': data['payment_frequency'] == constants.FREQUENCY_MONTHLY,
            'service': data['payment_method'],
            'transaction_id': data['transaction_id'],
            'project': data['project'],
            'last_4': data.get('last_4', None),
            'donation_url': data['landing_url'],
            'locale': data['locale'],
            'conversion_amount': data.get('settlement_amount', None),
        }
    })


class BraintreeWebhookProcessor:

    def process(self, notification):
        process_method = getattr(self, 'process_{}'.format(notification.kind), None)
        if process_method is not None:
            return process_method(notification)

    def process_subscription_charged_successfully(self, notification):
        last_tx = notification.subscription.transactions[0]
        is_paypal = last_tx.payment_instrument_type == 'paypal_account'

        # Custom fields are stored against the customer, and it requires a few
        # steps to get this object from Braintree
        payment_method = gateway.payment_method.find(notification.subscription.payment_method_token)
        customer = gateway.customer.find(payment_method.customer_id)
        custom_fields = customer.custom_fields or {}

        # The details of a donor are in a different spot depending on the payment method

        if is_paypal:
            donor_details = {
                "last_name": last_tx.paypal_details.payer_last_name,
                "first_name": last_tx.paypal_details.payer_first_name,
                "email": last_tx.paypal_details.payer_email
            }
        elif last_tx.payment_instrument_type == 'credit_card':
            donor_details = {
                'last_name': last_tx.customer_details.last_name,
                'first_name': last_tx.customer_details.first_name,
                'email': last_tx.customer_details.email,
            }
        else:
            logger.error(f"Unexpected payment type on subscription webhook: {last_tx.payment_instrument_type}")

        send_transaction_to_basket({
            'last_name': donor_details.get('last_name', ''),
            'first_name': donor_details.get('first_name', ''),
            'campaign_id': custom_fields.get('campaign_id', ''),
            'email': donor_details.get('email', ''),
            'amount': last_tx.amount,
            'currency': last_tx.currency_iso_code.lower(),
            'payment_frequency': constants.FREQUENCY_MONTHLY,
            'payment_method': constants.METHOD_PAYPAL if is_paypal else constants.METHOD_CARD,
            'transaction_id': last_tx.id,
            'project': custom_fields.get('project', ''),
            'last_4': None if is_paypal else last_tx.credit_card_details.last_4,
            'landing_url': '',
            'locale': custom_fields.get('locale', ''),
            'settlement_amount': last_tx.disbursement_details.settlement_amount,
        })

    def process_subscription_charged_unsuccessfully(self, notification):
        send_to_sqs({
            'data': {
                'event_type': 'charge.failed',
                'transaction_id': notification.subscription.id,
                'failure_code': notification.subscription.transactions[0].status,
            }
        })

    def process_dispute_lost(self, notification):
        send_to_sqs({
            'data': {
                'event_type': 'charge.dispute.closed',
                'status': 'lost',
                'transaction_id': notification.dispute.transaction.id,
                'failure_code': notification.dispute.reason,
            }
        })


def process_webhook(form_data):
    notification = gateway.webhook_notification.parse(form_data['bt_signature'], form_data['bt_payload'])
    BraintreeWebhookProcessor().process(notification)
