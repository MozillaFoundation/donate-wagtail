from functools import lru_cache
import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

import boto3


@lru_cache(maxsize=1)
def sqs_client():
    if all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION]):
        return boto3.client(
            'sqs',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )


def send_to_sqs(payload):
    # If BASKET_SQS_QUEUE_URL is not configured, do nothing (djangorq is logging the payload).
    if settings.BASKET_SQS_QUEUE_URL:
        client = sqs_client()
        if client is None:
            return

        return client.send_message(
            QueueUrl=settings.BASKET_SQS_QUEUE_URL,
            MessageBody=json.dumps(payload, cls=DjangoJSONEncoder, sort_keys=True),
        )
