import logging
import time
import json
from django.conf import settings

import django_rq
import requests
import stripe

from . import constants, gateway
from .sqs import send_to_sqs
from .utils import zero_decimal_currency_fix


logger = logging.getLogger(__name__)

queue = django_rq.get_queue('default')

BASKET_NEWSLETTER_API_PATH = '/news/subscribe/'
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET
stripe.api_key = settings.STRIPE_API_KEY


def send_stripe_transaction_to_basket(subscription, charge, metadata,
                                      donation_url, conversion_amount,
                                      net_amount, transaction_fee):
    project = 'mozillafoundation'

    if metadata.thunderbird:
        project = 'thunderbird'
    elif metadata.glassroomnyc:
        project = 'glassroomnyc'

    send_to_sqs({
        'data': {
            'event_type': 'donation',
            'last_name': subscription.customer.sources.data[0]['name'],
            'email': subscription.customer.email,
            'donation_amount': zero_decimal_currency_fix(charge.amount, charge.currency),
            'currency': charge.currency,
            'created': charge.created,
            'recurring': True,
            'frequency': 'monthly',
            'service': 'stripe',
            'transaction_id': charge.id,
            'subscription_id': subscription.id,
            'donation_url': donation_url,
            'project': project,
            'locale': subscription.metadata.locale,
            'last_4': subscription.customer.sources.data[0]['last4'],
            'conversion_amount': conversion_amount,
            'net_amount': net_amount,
            'transaction_fee': transaction_fee
        }
    })


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
            'subscription_id': data.get('subscription_id', None),
            'project': data['project'],
            'last_4': data.get('last_4', None),
            'donation_url': data['landing_url'],
            'locale': data['locale'],
            'conversion_amount': data.get('settlement_amount', None),
        }
    })


class BraintreeWebhookProcessor:

    def process(self, notification):
        process_method = getattr(self, f'process_{notification.kind}')
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
            'subscription_id': notification.subscription.id,
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


class StripeWebhookProcessor:
    def process(self, event):
        # Stripe event types use dot-notation, so convert periods to underscores
        event_type = event.type.replace('.', '_')

        try:
            process_method = getattr(self, f'process_{event_type}')
        except AttributeError:
            logger.info(f'An unsupported Stripe event was not processed: {event_type}')
            return

        if process_method is not None:
            return process_method(event)

    def process_charge_succeeded(self, event):
        charge_id = event.data.object.id
        try:
            charge = stripe.Charge.retrieve(
                charge_id,
                expand=['invoice', 'balance_transaction']
            )
        except stripe.error.StripeError as e:
            logger.error(f'Error fetching Stripe Charge: {e._message}', exc_info=True)
            return

        if not charge.invoice or not charge.invoice.subscription:
            logger.info('This charge is not associated with a subscription')
            return

        balance_transaction = charge.balance_transaction
        conversion_amount = balance_transaction.amount / 100
        net_amount = balance_transaction.net / 100
        transaction_fee = balance_transaction.fee / 100

        subscription_id = charge.invoice.subscription

        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
        except stripe.error.StripeError as e:
            logger.error(f'Error fetching Stripe Subscription: {e._message}', exc_info=True)
            return

        metadata = subscription.metadata
        update_data = {'metadata': metadata}
        donation_url = None

        if metadata.donation_url:
            donation_url = metadata.donation_url

        if metadata.thunderbird:
            update_data['description'] = 'Thunderbird monthly'
        elif metadata.glassroomnyc:
            update_data['description'] = 'glassroomnyc monthly'
        else:
            update_data['description'] = 'Mozilla Foundation Monthly Donation'

        try:
            stripe.Charge.modify(charge_id, update_data)
        except stripe.error.StripeError as e:
            logger.error(f'Error updating Stripe Charge description and metadata: {e._message}', exc_info=True)
            return

        send_stripe_transaction_to_basket(
            subscription,
            charge,
            metadata,
            donation_url,
            conversion_amount,
            net_amount,
            transaction_fee,
        )

        # queue.enqueue(self.upgrade_stripe_subscription_to_braintree, {
        #     'charge': charge,
        #     'subscription': subscription,
        # })

    # def upgrade_stripe_subscription_to_braintree(self, charge_data):
    #     charge = charge_data['charge']
    #     subscription = charge_data['subscription']
    #
    #     try:
    #         customer = stripe.Customer.retrieve(charge.customer)
    #     except stripe.error.StripeError as e:
    #         logger.error(f'Error fetching Stripe Subscription: {e._message}', exc_info=True)
    #         return
    #
    #     try:
    #         payment_method = stripe.PaymentMethod.retrieve(charge.payment_method)
    #     except stripe.error.StripeError as e:
    #         logger.error(f'Error fetching payment method: {e._message}', exc_info=True)

        # 1. Grab customer ID
        # 2. Lookup in logs what token is associated with customer ID
        # 3. Create a new sub in BT starting the next month for the same currency and amount, using the PMT
        # 4. Once successfully created, Cancel the Stripe Subscription (optional quest: update subscription metadata with note about the migration, include the BT subscription ID)
        # 5. If #3 fails, do not do 4; if 4 fails, CANCEL 3; if that fails, SOUND THE ALARM
        # 6. Possible other cleanup tasks, not sure. DO NOT DELETE CUSTOMER OBJ

        # gateway.subscription.create({
        #     'payment_method_token': 'PLACEHOLDER',
        #     'plan_id': 'PLACEHOLDER'
        # })



def process_webhook(form_data):
    notification = gateway.webhook_notification.parse(form_data['bt_signature'], form_data['bt_payload'])
    BraintreeWebhookProcessor().process(notification)


def process_stripe_webhook(form_data, signature=None):
    if not signature:
        logger.error('No signature provided', exc_info=True)
        return

    try:
        event = stripe.Event.construct_from(
            json.loads(form_data),
            signature,
            STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error('Request payload invalid', exc_info=True)
        return
    except stripe.error.SignatureVerificationError:
        logger.error('Request signature invalid', exc_info=True)
        return

    StripeWebhookProcessor().process(event)
