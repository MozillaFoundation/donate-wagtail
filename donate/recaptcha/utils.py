import logging

from django.conf import settings

import requests
from requests.exceptions import RequestException

API_URL = 'https://www.google.com/recaptcha/api/siteverify'
logger = logging.getLogger(__name__)


def verify(token):
    # this is only used for the (card based) donate form,
    # as verifying in donate.recaptcha.fields.ReCaptchaField

    secret = settings.RECAPTCHA_SECRET_KEY_CHECKBOX
    try:
        response = requests.post(API_URL, timeout=5, data={
            'secret': secret,
            'response': token
        })
        response.raise_for_status()
    except RequestException:
        logger.exception('Failed to make request to recaptcha API')
        return True

    return response.json()['success']
