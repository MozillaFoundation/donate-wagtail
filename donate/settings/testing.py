from configurations import Configuration
from .base import Base
from .secure import Secure
from .redis import Redis
from .oidc import OIDC
from .database import Database
from .braintree import Braintree


class Testing(Base, Secure, Redis, OIDC, Database, Braintree, Configuration):
    SECRET_KEY = 'test'
    RECAPTCHA_ENABLED = False
    RECAPTCHA_SITE_KEY = 'test'
    RECAPTCHA_SECRET_KEY = 'test'

    BRAINTREE_MERCHANT_ID = 'test'
    BRAINTREE_PRIVATE_KEY = 'test'
    BRAINTREE_PUBLIC_KEY = 'test'
    BRAINTREE_USE_SANDBOX = True
    BRAINTREE_MERCHANT_ACCOUNTS = {
        'usd': 'usd-ac',
        'gbp': 'gbp-ac',
    }
    BRAINTREE_PLANS = {
        'usd': 'usd-plan',
        'gbp': 'gbp-plan',
    }

    BASKET_API_ROOT_URL = 'http://localhost'
    BASKET_SQS_QUEUE_URL = 'sqs.us-east-1.amazonaws.com/1234567890/test'
    AWS_REGION = 'us-east-1'
    AWS_STORAGE_BUCKET_NAME = 'test'

    HEROKU_APP_NAME = None

    @classmethod
    def pre_setup(cls):
        super().pre_setup()

    @classmethod
    def setup(cls):
        super().setup()

    @classmethod
    def post_setup(cls):
        super().post_setup()
