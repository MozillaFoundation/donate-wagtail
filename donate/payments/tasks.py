import json
import logging
import time

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

import requests
from rq import Queue
from worker import conn

from . import constants
from .sqs import sqs_client


logger = logging.getLogger(__name__)

queue = Queue(connection=conn)

BASKET_NEWSLETTER_API_PATH = '/news/subscribe'


def send_newsletter_subscription_to_basket(data):
    if settings.BASKET_API_ROOT_URL is None:
        return

    url = f'{settings.BASKET_API_ROOT_URL}{BASKET_NEWSLETTER_API_PATH}'
    payload = {
        'format': 'html',
        'lang': data['lang'],
        'newsletters': 'mozilla-foundation',
        'trigger_welcome': 'N',
        'source_url': data['source_url'],
        'email': data['email']
    }
    try:
        return requests.post(url, json=payload)
    except requests.exceptions.RequestException:
        logger.exception('Failed to post to basket newsletter API')


def send_transaction_to_basket(data):
    client = sqs_client()
    if client is None:
        return

    payload = {
        'event_type': 'donation',
        'last_name': data['last_name'],
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

    client.send_message(
        QueueUrl=settings.BASKET_SQS_QUEUE_URL,
        MessageBody=json.dumps(payload, cls=DjangoJSONEncoder, sort_keys=True),
    )
