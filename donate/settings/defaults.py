import environ

app = environ.Path(__file__) - 2

CSP_DEFAULT_SRC = ("'self'")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", 'www.google-analytics.com',
                  'js.braintreegateway.com', 'assets.braintreegateway.com',
                  'www.paypalobjects.com', 'c.paypal.com', 'www.paypal.com')
CSP_IMG_SRC = ('*', "data:")
CSP_FONT_SRC = ("'self'", 'fonts.googleapis.com', 'fonts.gstatic.com')
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", 'https://fonts.googleapis.com', 'https://fonts.gstatic.com')
CSP_FRAME_SRC = ("'self'", 'assets.braintreegateway.com', 'c.paypal.com', '*.paypal.com')
CSP_CONNECT_SRC = ("'self'", 'api.sandbox.braintreegateway.com',
                   'client-analytics.sandbox.braintreegateway.com', 'api.braintreegateway.com',
                   'client-analytics.braintreegateway.com', '*.braintree-api.com', 'www.paypal.com',
                   'www.google-analytics.com', 'https://www.mozilla.org/en-US/newsletter/',
                   'https://sentry.prod.mozaws.net')
CSP_BASE_URI = CSP_DEFAULT_SRC
CSP_WORKER_SRC = CSP_DEFAULT_SRC

BRAINTREE_MERCHANT_ACCOUNTS = {
    'usd': 'mozillafoundation',
    'aud': 'MozillaFoundat_AUD',
    'brl': 'MozillaFoundat_BRL',
    'cad': 'MozillaFoundat_CAD',
    'chf': 'MozillaFoundat_CHF',
    'czk': 'MozillaFoundat_CZK',
    'dkk': 'MozillaFoundat_DKK',
    'eur': 'MozillaFoundat_EUR',
    'gbp': 'MozillaFoundat_GBP',
    'hkd': 'MozillaFoundat_HKD',
    'huf': 'MozillaFoundat_HUF',
    'inr': 'MozillaFoundat_INR',
    'jpy': 'MozillaFoundat_JPY',
    'mxn': 'MozillaFoundat_MXN',
    'nok': 'MozillaFoundat_NOK',
    'nzd': 'MozillaFoundat_NZD',
    'pln': 'MozillaFoundat_PLN',
    'rub': 'MozillaFoundat_RUB',
    'sek': 'MozillaFoundat_SEK',
    'twd': 'MozillaFoundat_TWD'
}
BRAINTREE_PLANS = {
    'brl': 'brl',
    'cad': 'cad',
    'chf': 'chf',
    'czk': 'czk',
    'dkk': 'dkk',
    'eur': 'eur',
    'gbp': 'gbp',
    'hkd': 'hkd',
    'huf': 'huf',
    'inr': 'inr',
    'jpy': 'jpy',
    'lak': 'lak',
    'mxn': 'mxn',
    'nok': 'nok',
    'nzd': 'nzd',
    'pln': 'pln',
    'rub': 'rub',
    'sek': 'sek',
    'twd': 'twd',
    'usd': 'usd'
}

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
        'rq_console': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '%H:%M:%S'
        }
    },
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler'
        },
        'debug-error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler'
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'rq_console': {
            'level': 'DEBUG',
            'class': 'rq.utils.ColorizingStreamHandler',
            'formatter': 'rq_console',
            'exclude': ['%(asctime)s']
        },
    },
    'loggers': {
        'django': {
            'handlers': ['debug'],
            'level': 'DEBUG'
        },
        'django.server': {
            'handlers': ['debug'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['error'],
            'propagate': False,
            'level': 'ERROR'
        },
        'django.template': {
            'handlers': ['debug-error'],
            'level': 'ERROR'
        },
        'django.db.backends': {
            'handlers': ['debug-error'],
            'level': 'ERROR'
        },
        'django.utils.autoreload': {
            'handlers': ['debug-error'],
            'level': 'ERROR'
        },
        'rq.worker': {
            'handlers': ['debug'],
            'level': 'DEBUG',
        },
        'donate': {
            'handlers': ['info'],
            'level': 'INFO',
        }
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            app('templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]
