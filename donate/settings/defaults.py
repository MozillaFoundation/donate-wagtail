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
    'aed': 'MozillaFoundat_AED',
    'aud': 'MozillaFoundat_AUD',
    'azn': 'MozillaFoundat_AZN',
    'bam': 'MozillaFoundat_BAM',
    'bdt': 'MozillaFoundat_BDT',
    'brl': 'MozillaFoundat_BRL',
    'cad': 'MozillaFoundat_CAD',
    'chf': 'MozillaFoundat_CHF',
    'clp': 'MozillaFoundat_CLP',
    'cny': 'MozillaFoundat_CNY',
    'czk': 'MozillaFoundat_CZK',
    'dkk': 'MozillaFoundat_DKK',
    'dzd': 'MozillaFoundat_DZD',
    'egp': 'MozillaFoundat_EGP',
    'eur': 'MozillaFoundat_EUR',
    'gbp': 'MozillaFoundat_GBP',
    'gel': 'MozillaFoundat_GEL',
    'gtq': 'MozillaFoundat_GTQ',
    'hkd': 'MozillaFoundat_HKD',
    'hrk': 'MozillaFoundat_HRK',
    'huf': 'MozillaFoundat_HUF',
    'idr': 'MozillaFoundat_IDR',
    'ils': 'MozillaFoundat_ILS',
    'inr': 'MozillaFoundat_INR',
    'jpy': 'MozillaFoundat_JPY',
    'krw': 'MozillaFoundat_KRW',
    'lak': 'MozillaFoundat_LAK',
    'lbp': 'MozillaFoundat_LBP',
    'mad': 'MozillaFoundat_MAD',
    'mxn': 'MozillaFoundat_MXN',
    'myr': 'MozillaFoundat_MYR',
    'nok': 'MozillaFoundat_NOK',
    'nzd': 'MozillaFoundat_NZD',
    'php': 'MozillaFoundat_PHP',
    'pln': 'MozillaFoundat_PLN',
    'qar': 'MozillaFoundat_QAR',
    'ron': 'MozillaFoundat_RON',
    'rub': 'MozillaFoundat_RUB',
    'sar': 'MozillaFoundat_SAR',
    'sek': 'MozillaFoundat_SEK',
    'sgd': 'MozillaFoundat_SGD',
    'thb': 'MozillaFoundat_THB',
    'try': 'MozillaFoundat_TRY',
    'twd': 'MozillaFoundat_TWD',
    'uah': 'MozillaFoundat_UAH',
    'yer': 'MozillaFoundat_YER',
    'zar': 'MozillaFoundat_ZAR'
}
BRAINTREE_PLANS = {
    'aed': 'aed',
    'aud': 'aud',
    'azn': 'azn',
    'bam': 'bam',
    'bdt': 'bdt',
    'brl': 'brl',
    'cad': 'cad',
    'chf': 'chf',
    'clp': 'clp',
    'cny': 'cny',
    'czk': 'czk',
    'dkk': 'dkk',
    'dzd': 'dzd',
    'egp': 'egp',
    'eur': 'eur',
    'gbp': 'gbp',
    'gel': 'gel',
    'gtq': 'gtq',
    'hkd': 'hkd',
    'hrk': 'hrk',
    'huf': 'huf',
    'idr': 'idr',
    'ils': 'ils',
    'inr': 'inr',
    'jpy': 'jpy',
    'krw': 'krw',
    'lak': 'lak',
    'lbp': 'lbp',
    'mad': 'mad',
    'mxn': 'mxn',
    'myr': 'myr',
    'nok': 'nok',
    'nzd': 'nzd',
    'php': 'php',
    'pln': 'pln',
    'qar': 'qar',
    'ron': 'ron',
    'rub': 'rub',
    'sar': 'sar',
    'sek': 'sek',
    'sgd': 'sgd',
    'thb': 'thb',
    'try': 'try',
    'twd': 'twd',
    'uah': 'uah',
    'yer': 'yer',
    'zar': 'zar',
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

RQ_QUEUES = {
    'default': {
        'URL': 'redis://redis:6379/0',
        'DEFAULT_TIMEOUT': 500,
    },

    # Must be a separate queue as it's limited to one item at a time
    'wagtail_localize_pontoon.sync': {
        'URL': 'redis://redis:6379/0',
        'DEFAULT_TIMEOUT': 500,
    },
}
