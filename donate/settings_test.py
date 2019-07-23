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


CURRENCIES = {
    'usd': {
        'code': 'usd',
        'minAmount': 2,
        'symbol': '$',
        'monthlyUpgrade': [
            {'min': 250, 'value': 30},
            {'min': 120, 'value': 20},
            {'min': 60, 'value': 15},
            {'min': 35, 'value': 10},
            {'min': 15, 'value': 5}
        ],
        'presets': {
            'single': [50, 25, 10, 3],
            'monthly': [10, 5, 3, 2]
        }
    },
    'gbp': {
        'code': 'gbp',
        'minAmount': 2,
        'symbol': '£',
        'monthlyUpgrade': [
            {'min': 250, 'value': 30},
            {'min': 120, 'value': 20},
            {'min': 60, 'value': 15},
            {'min': 35, 'value': 10},
            {'min': 15, 'value': 5}
        ],
        'presets': {
            'single': [50, 25, 10, 3],
            'monthly': [10, 5, 3, 2]
        }
    },
}
