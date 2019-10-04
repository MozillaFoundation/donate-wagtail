from .settings import *     # noqa

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
