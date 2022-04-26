from functools import lru_cache
import json
import logging
import time
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

import botocore
import boto3

logger = logging.getLogger(__name__)


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
    send_message_retries = 3
    # If BASKET_SQS_QUEUE_URL is not configured, do nothing (djangorq is logging the payload).
    if settings.BASKET_SQS_QUEUE_URL:
        client = sqs_client()
        if client is None:
            logger.error("Could not connect to SQS Client.")
            return

    for n in range(send_message_retries):
        try:
            client.send_message(
                QueueUrl=settings.BASKET_SQS_QUEUE_URL,
                MessageBody=json.dumps(payload, cls=DjangoJSONEncoder, sort_keys=True),
            )

            break

        except botocore.exceptions.ClientError as err:
            # Logging details on why the sqs client could not send the message
            logger.error('Error Message: {}'.format(err.response['Error']['Message']))
            time.sleep(5)
            continue
