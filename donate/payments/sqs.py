from functools import lru_cache
import json
import logging
from time import time, sleep
import sched
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

import botocore
import boto3

logger = logging.getLogger(__name__)
schedule = sched.scheduler(time, sleep)


@lru_cache(maxsize=1)
def sqs_client():
    if all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION]):
        return boto3.client(
            'sqs',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )


def attempt_send_to_sqs(client, payload):
    client.send_message(
        QueueUrl=settings.BASKET_SQS_QUEUE_URL,
        MessageBody=json.dumps(payload, cls=DjangoJSONEncoder, sort_keys=True),
    )


def send_to_sqs(payload):
    # If BASKET_SQS_QUEUE_URL is not configured, do nothing (djangorq is logging the payload).
    if settings.BASKET_SQS_QUEUE_URL:
        client = sqs_client()
        if client is None:
            logger.error("Could not connect to SQS Client.")
            return

    send_retries = 3
    send_data_immediately = 0  # seconds
    send_data_delay = 10  # seconds
    schedule_priority = 1
    call_args = (client, payload)

    for attempt in range(send_retries):
        if attempt == 0:
            schedule.enter(send_data_immediately, schedule_priority, attempt_send_to_sqs, call_args)
        else:
            schedule.enter(send_data_delay, schedule_priority, attempt_send_to_sqs, call_args)
        try:
            # explicitly block, just in case the implicit behaviour changes in the future
            schedule.run(blocking=True)
            break
        except botocore.exceptions.ClientError as err:
            if attempt != 2:
                logger.error(f"Error when sending data to SQS: {err}")
            else:
                logger.error(f"Could not send data to SQS. Unable to connect after {send_retries} retries.")

            continue
