from functools import lru_cache

from django.conf import settings

import boto3


@lru_cache(maxsize=1)
def sqs_client():
    if all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_LOCATION]):
        return boto3.client(
            'sqs',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_LOCATION
        )
