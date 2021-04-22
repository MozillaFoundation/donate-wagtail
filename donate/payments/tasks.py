import logging
import time
from decimal import Decimal

from django.conf import settings
from django.utils.timezone import datetime, timedelta

import django_rq
import requests
import stripe

from ..utility.acoustic.acoustic import acoustic_tx
from . import constants, gateway
from .sqs import send_to_sqs
from .utils import (
    zero_decimal_currency_fix,
    get_plan_id,
    get_merchant_account_id_for_card
)

logger = logging.getLogger(__name__)

queue = django_rq.get_queue('default')

BASKET_NEWSLETTER_API_PATH = '/news/subscribe/'
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET
stripe.api_key = settings.STRIPE_API_KEY


# The following 4 functions are used in "process_donation_receipt" to create proper dates and currency amounts
def mofo_donation_receipt_datetime(ts):
    # convert unix timestamp to e.g. "Thursday, Feb 11, 2021 at 4:20pm (GMT-08:00)"
    ds = datetime.utcfromtimestamp(float(ts))
    return ds - timedelta(hours=8)


def mofo_donation_receipt_time_string(ds):
    """Return the date and time formatted as requested by MoFo"""
    return ds.strftime("%Y-%m-%d %H:%M")


def mofo_donation_receipt_day_of_month(ds):
    """Return the day of the month"""
    return ds.strftime("%d")


def mofo_donation_receipt_number_format(amount):
    return f"{float(amount):.2f}"


# Fields needed for acoustic API and donation receipt
DONATION_RECEIPT_FIELDS = [
    "created",
    "currency",
    "donation_amount",
    "email",
    "first_name",
    "last_name",
    "recurring",
    "transaction_id",
    "card_type",
    "last_4",
    "locale",
    "service",
    "project",
]

# map of incoming donation data field names -> email/acoustic field names
DONATION_RECEIPT_FIELDS_MAP = {
    "card_type": "cc_type",
    "last_4": "cc_last_4_digits",
    "locale": "donation_locale",
    "service": "payment_source",
}

# These are compared with the donating users locale, to tell the Acoustic API what language to send the email
LANGUAGE_IDS = {
    "ja": "1621701",
    "pl": "1621706",
    "pt-BR": "1621708",
    "cs": "1621689",
    "de": "1621691",
    "es": "1621695",
    "fr": "1621697",
    "en-US": "1621694",
}


# Acoustic receipt sending
def process_donation_receipt(donation_data):
    # Creating new object by looping through mandatory receipt fields from const dictionary,
    # and updating them to equal the data being received
    message_data = {k: v for k, v in donation_data.items() if k in DONATION_RECEIPT_FIELDS}
    email = message_data.pop("email")
    # If the donation data did not recieve a payment time, use the current time.
    created = message_data.get("created", int(time.time()))
    # The next 3 lines are formatting the date and time for the email
    created_dt = mofo_donation_receipt_datetime(created)
    message_data["created"] = mofo_donation_receipt_time_string(created_dt)
    message_data["day_of_month"] = mofo_donation_receipt_day_of_month(created_dt)
    recurring = message_data.get("recurring", False)
    message_data["payment_frequency"] = "Recurring" if recurring else "One-Time"
    # Getting the amount donated, and formatting it for email
    donation_amount = message_data.get("donation_amount", donation_data.get('amount'))
    message_data["donation_amount"] = mofo_donation_receipt_number_format(donation_amount)
    message_data["friendly_from_name"] = (
        "MZLA Thunderbird" if message_data["project"] == "thunderbird" else "Mozilla"
    )

    # convert some field names to match Acoustic API by looping through dict
    # and updating fields that match
    send_data = {
        DONATION_RECEIPT_FIELDS_MAP.get(k, k): v for k, v in message_data.items()
    }
    # using the LANGUAGE_IDS const, we are getting the correct localized version of the email
    # based on the users locality, if there is none, default to English.
    message_id = LANGUAGE_IDS.get(LANGUAGE_IDS[message_data["locale"]], LANGUAGE_IDS["en-US"])
    acoustic_tx.send_mail(
        email,
        message_id,
        send_data,
        # BCC is set to none because if you set it to anything else, you get a
        # "BCC is not allowed for this campaign" response.
        bcc=None,
        save_to_db=True,
    )


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
    if settings.DONATION_RECEIPT_METHOD == 'DONATE':
        process_donation_receipt(data)
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
            'card_type': data.get('card_type', 'Unknown'),
            'last_4': data.get('last_4', None),
            'donation_url': data['landing_url'],
            'locale': data['locale'],
            'conversion_amount': data.get('settlement_amount', None),
        }
    })


def process_dispute(event):
    dispute = event.data.object
    send_to_sqs({
        'data': {
            'event_type': event.type,
            'transaction_id': dispute.charge,
            'reason': dispute.reason,
            'status': dispute.status
        }
    })


class BraintreeWebhookProcessor:
    def process(self, notification):
        kind = notification.kind
        if kind == 'subscription_charged_successfully':
            self.subscription_charged_successfully(notification)
        elif kind == 'subscription_charged_unsuccessfully':
            self.subscription_charged_unsuccessfully(notification)
        elif kind == 'dispute_lost':
            self.dispute_lost(notification)

    def subscription_charged_successfully(self, notification):
        last_tx = notification.subscription.transactions[0]
        is_paypal = last_tx.payment_instrument_type == 'paypal_account'

        # Custom fields are stored against the customer, and it requires a few
        # steps to get this object from Braintree
        payment_method = gateway.payment_method.find(notification.subscription.payment_method_token)
        customer = gateway.customer.find(payment_method.customer_id)

        custom_fields = customer.custom_fields or {}

        # If a customer record doesn't contain a project custom_field, update it to "mozillafoundation".
        # The customer was imported into Braintree from Stripe during the transition in late 2019.
        # Customers imported into Braintree in this way did not get the 'project' custom_field because it
        # is stored on the subscription object in Stripe's APIs. We can safely assume this is a Mozilla
        # Foundation recurring donation because we did not use the imported customers and their associated
        # vault information to recreate Thunderbird donations, due to the creation of MZLA
        if not custom_fields.get('project'):
            custom_fields['project'] = 'mozillafoundation'

            customer_update_result = gateway.customer.update(customer.id, {
                'custom_fields': custom_fields
            })

            if not customer_update_result.is_success:
                message = f'Failed to update a Braintree customer with a project custom_field: {customer.id}'
                print(message)
                logger.error(message, exc_info=True)
                return

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
            'card_type': 'Unknown' if is_paypal else last_tx.credit_card_details.card_type,
            'last_4': None if is_paypal else last_tx.credit_card_details.last_4,
            'landing_url': custom_fields.get('landing_url', ''),
            'locale': custom_fields.get('locale', ''),
            'settlement_amount': last_tx.disbursement_details.settlement_amount,
        })

    def subscription_charged_unsuccessfully(self, notification):
        send_to_sqs({
            'data': {
                'event_type': 'charge.failed',
                'transaction_id': notification.subscription.id,
                'failure_code': notification.subscription.transactions[0].status,
            }
        })

    def dispute_lost(self, notification):
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

    @staticmethod
    def process_charge_succeeded(event):
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
            subscription = stripe.Subscription.retrieve(subscription_id, expand=['customer'])
        except stripe.error.StripeError as e:
            logger.error(f'Error fetching Stripe Subscription: {e._message}', exc_info=True)
            return

        metadata = subscription.metadata
        donation_url = None

        if 'donation_url' in metadata:
            donation_url = metadata['donation_url']

        if 'thunderbird' in metadata:
            description = 'Thunderbird monthly'
        elif 'glassroomnyc' in metadata:
            description = 'glassroomnyc monthly'
        else:
            description = 'Mozilla Foundation Monthly Donation'

        try:
            stripe.Charge.modify(charge_id, metadata=metadata, description=description)
        except stripe.error.StripeError as e:
            logger.error(f'Error updating Stripe Charge description and metadata: {e._message}', exc_info=True)
            return

        project = 'mozillafoundation'

        if 'thunderbird' in metadata:
            project = 'thunderbird'
        elif 'glassroomnyc' in metadata:
            project = 'glassroomnyc'

        donation_data = {
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
        send_to_sqs(
            {'data': donation_data}
        )
        if settings.DONATION_RECEIPT_METHOD == 'DONATE':
            process_donation_receipt(donation_data)

        if settings.MIGRATE_STRIPE_SUBSCRIPTIONS_ENABLED and 'thunderbird' not in metadata:
            MigrateStripeSubscription().process(charge, subscription)

    @staticmethod
    def process_charge_dispute_closed(event):
        process_dispute(event)

    @staticmethod
    def process_charge_dispute_created(event):
        dispute = event.data.object
        if settings.AUTO_CLOSE_STRIPE_DISPUTES and dispute.status != 'lost':
            try:
                stripe.Dispute.close(dispute.id)
            except stripe.error.StripeError as e:
                logger.error(f'Error closing dispute {dispute.id}: {e._message}', exc_info=True)

        process_dispute(event)

    @staticmethod
    def process_charge_dispute_updated(event):
        process_dispute(event)

    @staticmethod
    def process_charge_refunded(event):
        charge = event.data.object
        refund = charge.refunds.data[0]
        reason = refund.reason

        # If there's no reason, we can assume the refund was made by donor care via the Stripe Dashboard
        if not reason:
            reason = 'requested_by_customer'

        send_to_sqs({
            'data': {
                'event_type': event.type,
                'transaction_id': charge.id,
                'reason': reason,
                'status': refund.status
            }
        })

    @staticmethod
    def process_charge_failed(event):
        charge = event.data.object

        if not charge.invoice:
            logger.info('This charge is not associated with a subscription')
            return

        try:
            invoice = stripe.Invoice.retrieve(charge.invoice, expand=['subscription.customer'])
        except stripe.error.StripeError as e:
            logger.error(f'Error fetching Stripe Invoice: {e._message}', exc_info=True)
            return

        subscription = invoice.subscription
        metadata = subscription.metadata
        failure_code = charge.failure_code

        donation_url = None
        if 'donation_url' in metadata:
            donation_url = metadata['donation_url']

        project = 'mozillafoundation'
        if 'thunderbird' in metadata:
            project = 'thunderbird'
        elif 'glassroomnyc' in metadata:
            project = 'glassroomnyc'

        send_to_sqs({
            'data': {
                'transaction_id': charge.id,
                'subscription_id': subscription.id,
                'event_type': event.type,
                'last_name': subscription.customer.sources.data[0]['name'],
                'email': subscription.customer.email,
                'donation_amount': zero_decimal_currency_fix(charge.amount, charge.currency),
                'currency': charge.currency,
                'created': charge.created,
                'recurring': True,
                'frequency': 'monthly',
                'service': 'stripe',
                'donation_url': donation_url,
                'project': project,
                'locale': subscription.metadata.locale,
                'last_4': subscription.customer.sources.data[0]['last4'],
                'failure_code': failure_code
            }
        })


class MigrateStripeSubscription:
    def process(self, charge, subscription):
        # Grab the payment card ID from the subscription's payment source list (there will only be one)
        card_id = subscription.customer.sources.data[0].id

        # Confirm the payment method was migrated to Braintree by looking up
        # BT Payment Methods using the Stripe card ID
        payment_method = gateway.payment_method.find(card_id)

        # Ensure we found a Payment Method, and if not, report it to Sentry as an error
        if not payment_method:
            message = f'The payment method was not migrated to' \
                      f' Braintree for this charge: {charge.id}'
            print(message)
            logger.error(message, exc_info=True)
            return

        # Determine the Braintree plan, merchant account, and price
        # for the subscription based on the subscription's attributes
        BT_plan_id = get_plan_id(charge.currency)
        BT_merchant_account = get_merchant_account_id_for_card(charge.currency)
        BT_price = Decimal(zero_decimal_currency_fix(charge.amount, charge.currency))
        BT_first_billing_date = datetime.utcfromtimestamp(subscription.current_period_end)

        # Create the Braintree subscription and record the result for analysis
        BT_create_subscription_result = gateway.subscription.create({
            'payment_method_token': payment_method.token,
            'plan_id': BT_plan_id,
            'merchant_account_id': BT_merchant_account,
            'price': BT_price,
            'first_billing_date': BT_first_billing_date
        })

        # If the subscription creation failed, record the error in Sentry
        if not BT_create_subscription_result.is_success:
            message = f'Failed to create a Braintree subscription from Stripe subscription {subscription.id}'
            print(message)
            logger.error(message, exc_info=True)
            logger.error(BT_create_subscription_result.message)
            # this might not exist
            if BT_create_subscription_result.errors:
                logger.error(BT_create_subscription_result.errors)
            return

        # Cancel Stripe subscription
        try:
            stripe.Subscription.delete(subscription.id)
        except stripe.error.StripeError:
            message = f'Failed to cancel the stripe subscription ' \
                      f'{subscription.id}, cancelling the Braintree subscription'
            print(message)
            logger.error(message, exc_info=True)

            # Cancel the subscription that we just created since the Stripe subscription cancellation failed.
            BT_cancel_subscription_result = gateway.subscription.cancel(
                BT_create_subscription_result.subscription.id
            )

            # if this fails, we're really screwed, so make it a critical log now that the
            # customer has two active subscriptions
            if not BT_cancel_subscription_result.is_success:
                message = f'Failed to cancel the Braintree Subscription, ' \
                          f'customer now has two active subscriptions - ' \
                          f'Braintree: {BT_create_subscription_result.subscription.id}, ' \
                          f'Stripe: {subscription.id}'
                print(message)
                logger.critical(message)


def process_webhook(form_data):
    """
    Called in response to a BrainTree webhook for successful subscription transaction
    (e.g. monthly / monthly upsell)
    """
    notification = gateway.webhook_notification.parse(form_data['bt_signature'], form_data['bt_payload'])
    BraintreeWebhookProcessor().process(notification)


def process_stripe_webhook(form_data, signature=None):
    try:
        event = stripe.Event.construct_from(
            form_data,
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
