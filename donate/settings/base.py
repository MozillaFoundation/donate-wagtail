import django
import logging.config
import sys
from . import defaults
from .environment import (
    env,
    app,
    root
)

from .languages import LANGUAGES, LANGUAGE_IDS


class Base(object):
    SECRET_KEY = env('DJANGO_SECRET_KEY')
    WAGTAIL_SITE_NAME = 'donate'
    WSGI_APPLICATION = 'donate.wsgi.application'
    LANGUAGE_CODE = 'en-US'
    LANGUAGE_IDS = LANGUAGE_IDS
    DEFAULT_LANGUAGE_ID = LANGUAGE_IDS[LANGUAGE_CODE]
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    AUTH_USER_MODEL = 'users.User'
    ALLOWED_HOSTS = env('ALLOWED_HOSTS')
    RANDOM_SEED = env('RANDOM_SEED')
    ENABLE_THUNDERBIRD_REDIRECT = env('ENABLE_THUNDERBIRD_REDIRECT')

    # Kount custom field value (overridden by TBird config)
    # https://github.com/mozilla/donate-wagtail/issues/934
    # https://github.com/mozilla/donate-wagtail/issues/1033
    FRAUD_SITE_ID = 'mofo'

    # Domain Redirects
    DOMAIN_REDIRECT_MIDDLEWARE_ENABLED = env('DOMAIN_REDIRECT_MIDDLEWARE_ENABLED')
    TARGET_DOMAINS = env('TARGET_DOMAINS')

    # Acoustic Configuration
    ACOUSTIC_TX_CLIENT_ID = env('ACOUSTIC_TX_CLIENT_ID')
    ACOUSTIC_TX_CLIENT_SECRET = env('ACOUSTIC_TX_CLIENT_SECRET')
    ACOUSTIC_TX_REFRESH_TOKEN = env('ACOUSTIC_TX_REFRESH_TOKEN')
    ACOUSTIC_TX_SERVER_NUMBER = env('ACOUSTIC_TX_SERVER_NUMBER')
    DONATION_RECEIPT_METHOD = env('DONATION_RECEIPT_METHOD')

    # Basket Configuration
    BASKET_API_ROOT_URL = env('BASKET_API_ROOT_URL')
    BASKET_SQS_QUEUE_URL = env('BASKET_SQS_QUEUE_URL')
    # Basket client configuration
    BASKET_URL = env('BASKET_URL')

    # Pontoon settings
    WAGTAILLOCALIZE_GIT_SYNC_MANAGER_CLASS = 'donate.core.pontoon.CustomSyncManager'
    WAGTAILLOCALIZE_GIT_URL = env('WAGTAILLOCALIZE_PONTOON_GIT_URL')
    WAGTAILLOCALIZE_GIT_DEFAULT_BRANCH = env('WAGTAILLOCALIZE_PONTOON_GIT_DEFAULT_BRANCH')
    WAGTAILLOCALIZE_GIT_CLONE_DIR = env('WAGTAILLOCALIZE_PONTOON_GIT_CLONE_DIR')
    SSH_KEY = env('SSH_KEY')
    SSH_CONFIG = env('SSH_CONFIG')

    # Static content settings
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATICFILES_DIRS = [app('frontend')]
    STATIC_ROOT = root('static')
    STATIC_URL = '/static/'

    MEDIA_ROOT = root('media/')
    MEDIA_URL = '/media/'

    # Stripe webhook credentials
    STRIPE_API_KEY = env('STRIPE_API_KEY')
    STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET')
    AUTO_CLOSE_STRIPE_DISPUTES = env('AUTO_CLOSE_STRIPE_DISPUTES')
    MIGRATE_STRIPE_SUBSCRIPTIONS_ENABLED = env('MIGRATE_STRIPE_SUBSCRIPTIONS_ENABLED')

    # Thunderbird mailchimp API key
    THUNDERBIRD_MC_API_KEY = env('THUNDERBIRD_MC_API_KEY')
    THUNDERBIRD_MC_SERVER = env('THUNDERBIRD_MC_SERVER')
    THUNDERBIRD_MC_LIST_ID = env('THUNDERBIRD_MC_LIST_ID')

    LOCALE_PATHS = [
        app('locale'),
    ]

    # Review apps' slack bot
    GITHUB_TOKEN = env('GITHUB_TOKEN')
    SLACK_WEBHOOK_RA = env('SLACK_WEBHOOK_RA')

    # Pontoon check slack bot
    SLACK_WEBHOOK_PONTOON = env('SLACK_WEBHOOK_PONTOON')
    TRAVIS_LOGS_URL = env('TRAVIS_JOB_WEB_URL', default='')

    # Detect if Django is running normally, or in test mode through "manage.py test"
    TESTING = 'test' in sys.argv

    @property
    def CSRF_TRUSTED_ORIGINS(self):
        return self.ALLOWED_HOSTS

    INSTALLED_APPS = [
        'whitenoise.runserver_nostatic',
        'scout_apm.django',

        'donate.users',
        'donate.core',
        'donate.payments',
        'donate.recaptcha',

        'wagtail_localize',
        'wagtail_localize.locales',
        'wagtail_localize_git',
        'wagtail_ab_testing',

        'wagtail.contrib.forms',  # Temporarily needed as wagtail-ab-testing imports it
        'wagtail.contrib.redirects',
        'wagtail.contrib.settings',
        'wagtail.contrib.legacy.richtext',  # Must be before 'wagtail.core'
        'wagtail.embeds',
        'wagtail.sites',
        'wagtail.users',
        'wagtail.snippets',
        'wagtail.documents',
        'wagtail.images',
        'wagtail.search',
        'wagtail.admin',
        'wagtail.core',

        'modelcluster',
        'taggit',
        'storages',
        'django_rq',
        'django_countries',

        'django.contrib.admin',
        'django.contrib.auth',
        'mozilla_django_oidc',

        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sitemaps',
    ]

    @property
    def MIDDLEWARE(self):
        return list(filter(None, [
            'django.middleware.security.SecurityMiddleware',
            'whitenoise.middleware.WhiteNoiseMiddleware',
            'donate.utility.middleware.TargetDomainRedirectMiddleware'
            if self.DOMAIN_REDIRECT_MIDDLEWARE_ENABLED else None,
            'django.middleware.gzip.GZipMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'wagtail.contrib.redirects.middleware.RedirectMiddleware',
            'csp.middleware.CSPMiddleware',
            # Make sure to check for deauthentication during a session:
            'mozilla_django_oidc.middleware.SessionRefresh'
        ]))

    ROOT_URLCONF = 'donate.urls'

    TEMPLATES = defaults.TEMPLATES

    LANGUAGES = LANGUAGES
    WAGTAIL_CONTENT_LANGUAGES = LANGUAGES
    WAGTAIL_I18N_ENABLED = True

    # Logging Config
    LOGGING_CONFIG = None
    LOGGING = defaults.LOGGING

    CSP_DEFAULT_SRC = env('CSP_DEFAULT_SRC')
    CSP_BASE_URI = env('CSP_BASE_URI')
    CSP_CONNECT_SRC = env('CSP_CONNECT_SRC')
    CSP_FRAME_ANCESTORS = env('CSP_FRAME_ANCESTORS')
    CSP_FORM_ACTION = env('CSP_FORM_ACTION')
    CSP_REPORT_URI = env('CSP_REPORT_URI')
    CSP_OBJECT_SRC = env('CSP_OBJECT_SRC')
    CSP_MEDIA_SRC = env('CSP_MEDIA_SRC')
    CSP_FRAME_SRC = env('CSP_FRAME_SRC')
    CSP_SCRIPT_SRC = env('CSP_SCRIPT_SRC')
    CSP_IMG_SRC = env('CSP_IMG_SRC')
    CSP_FONT_SRC = env('CSP_FONT_SRC')
    CSP_STYLE_SRC = env('CSP_STYLE_SRC')
    CSP_WORKER_SRC = env('CSP_WORKER_SRC')
    CSP_INCLUDE_NONCE_IN = env('CSP_INCLUDE_NONCE_IN')

    FRONTEND = {
        'RELEASE_VERSION': env('HEROKU_RELEASE_VERSION'),
        'SENTRY_DSN': env('SENTRY_DSN'),
        'SENTRY_ENVIRONMENT': env('SENTRY_ENVIRONMENT'),
        'BRAINTREE_MERCHANT_ACCOUNTS': env('BRAINTREE_MERCHANT_ACCOUNTS'),
        'PAYPAL_DISPLAY_NAME': 'Mozilla Foundation'
    }

    CURRENCIES = {
        'usd': {
            'code': 'usd',
            'minAmount': {
                'single': 10,
                'monthly': 5,
            },
            'symbol': '$',
            'paypalFixedFee': {
                'macro': 0.30,
                'micro': 0.05
            },
            'monthlyUpgrade': [
                {'min': 300, 'value': 30},
                {'min': 200, 'value': 20},
                {'min': 100, 'value': 10},
                {'min': 70, 'value': 7},
                {'min': 35, 'value': 5},
                {'min': 15, 'value': 5},
            ],
            'presets': {
                'single': [10, 20, 30, 60],
                'monthly': [10, 15, 20, 25],
            }
        },
        'aud': {
            'code': 'aud',
            'minAmount': {
                'single': 10,
                'monthly': 10,
            },
            'symbol': '$',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 0.30,
                'micro': 0.05
            },
            'monthlyUpgrade': [
                {'min': 432, 'value': 40},
                {'min': 288, 'value': 30},
                {'min': 144, 'value': 15},
                {'min': 99, 'value': 10},
                {'min': 50, 'value': 10},
                {'min': 22, 'value': 10},
            ],
            'presets': {
                'single': [10, 20, 30, 60],
                'monthly': [10, 15, 20, 25],
            }
        },
        'brl': {
            'code': 'brl',
            'minAmount': {
                'single': 8,
                'monthly': 8,
            },
            'symbol': 'R$',
            'paypalFixedFee': {
                'macro': 0.60,
                'micro': 0.10
            },
            'disabled': ['amex'],
            'monthlyUpgrade': [
                {'min': 1137, 'value': 100},
                {'min': 758, 'value': 75},
                {'min': 379, 'value': 35},
                {'min': 265, 'value': 25},
                {'min': 133, 'value': 20},
                {'min': 57, 'value': 10},
            ],
            'presets': {
                'single': [80, 40, 20, 10],
                'monthly': [40, 20, 10, 8]
            }
        },
        'cad': {
            'code': 'cad',
            'minAmount': {
                'single': 10,
                'monthly': 10,
            },
            'symbol': '$',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 0.30,
                'micro': 0.05
            },
            'monthlyUpgrade': [
                {'min': 393, 'value': 40},
                {'min': 262, 'value': 25},
                {'min': 131, 'value': 12},
                {'min': 92, 'value': 10},
                {'min': 46, 'value': 10},
                {'min': 20, 'value': 10},
            ],
            'presets': {
                'single': [10, 20, 30, 60],
                'monthly': [10, 15, 20, 25],
            }
        },
        'chf': {
            'code': 'chf',
            'minAmount': {
                'single': 2,
                'monthly': 2,
            },
            'symbol': 'Fr.',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 0.55,
                'micro': 0.09
            },
            'monthlyUpgrade': [
                {'min': 297, 'value': 30},
                {'min': 198, 'value': 20},
                {'min': 99, 'value': 10},
                {'min': 69, 'value': 7},
                {'min': 35, 'value': 5},
                {'min': 15, 'value': 3},
            ],
            'presets': {
                'single': [10, 20, 30, 60],
                'monthly': [5, 10, 15, 20],
            }
        },
        'czk': {
            'code': 'czk',
            'minAmount': {
                'single': 45,
                'monthly': 45,
            },
            'symbol': 'Kč',
            'paypalFixedFee': {
                'macro': 10.00,
                'micro': 1.67
            },
            'disabled': ['amex'],
            'monthlyUpgrade': [
                {'min': 6870, 'value': 700},
                {'min': 4580, 'value': 450},
                {'min': 2290, 'value': 225},
                {'min': 1603, 'value': 150},
                {'min': 802, 'value': 100},
                {'min': 344, 'value': 65},
            ],
            'presets': {
                'single': [450, 220, 110, 70],
                'monthly': [220, 110, 70, 45]
            }
        },
        'dkk': {
            'code': 'dkk',
            'minAmount': {
                'single': 13,
                'monthly': 13,
            },
            'symbol': 'kr',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 2.60,
                'micro': 0.43
            },
            'monthlyUpgrade': [
                {'min': 2007, 'value': 200},
                {'min': 1338, 'value': 125},
                {'min': 669, 'value': 60},
                {'min': 468, 'value': 45},
                {'min': 234, 'value': 30},
                {'min': 100, 'value': 20},
            ],
            'presets': {
                'single': [130, 60, 30, 20],
                'monthly': [60, 30, 20, 15]
            }
        },
        'eur': {
            'code': 'eur',
            'minAmount': {
                'single': 10,
                'monthly': 5,
            },
            'symbol': '€',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 0.35,
                'micro': 0.05
            },
            'monthlyUpgrade': [
                {'min': 270, 'value': 25},
                {'min': 180, 'value': 20},
                {'min': 90, 'value': 10},
                {'min': 63, 'value': 6},
                {'min': 32, 'value': 5},
            ],
            'presets': {
                'single': [10, 20, 30, 60],
                'monthly': [10, 15, 20, 25],
            }
        },
        'gbp': {
            'code': 'gbp',
            'minAmount': {
                'single': 10,
                'monthly': 5,
            },
            'symbol': '£',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 0.20,
                'micro': 0.05
            },
            'monthlyUpgrade': [
                {'min': 240, 'value': 25},
                {'min': 160, 'value': 15},
                {'min': 80, 'value': 10},
                {'min': 56, 'value': 5},
                {'min': 28, 'value': 5},
                {'min': 12, 'value': 5},
            ],
            'presets': {
                'single': [10, 20, 30, 60],
                'monthly': [10, 15, 20, 25]
            }
        },
        'hkd': {
            'code': 'hkd',
            'minAmount': {
                'single': 15,
                'monthly': 15,
            },
            'symbol': '$',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 2.35,
                'micro': 0.39
            },
            'monthlyUpgrade': [
                {'min': 2343, 'value': 200},
                {'min': 1562, 'value': 150},
                {'min': 781, 'value': 75},
                {'min': 547, 'value': 50},
                {'min': 273, 'value': 40},
                {'min': 117, 'value': 25},
            ],
            'presets': {
                'single': [100, 50, 25, 18],
                'monthly': [70, 30, 20, 15]
            }
        },
        'huf': {
            'code': 'huf',
            'minAmount': {
                'single': 570,
                'monthly': 570,
            },
            'symbol': 'Ft',
            'paypalFixedFee': {
                'macro': 90,
                'micro': 15
            },
            'disabled': ['amex'],
            'monthlyUpgrade': [
                {'min': 87600, 'value': 8000},
                {'min': 58400, 'value': 5000},
                {'min': 29200, 'value': 3000},
                {'min': 20400, 'value': 2000},
                {'min': 10200, 'value': 1500},
                {'min': 4380, 'value': 900},
            ],
            'zeroDecimal': 'paypal',
            'presets': {
                'single': [5600, 2800, 1400, 850],
                'monthly': [2800, 1400, 850, 600]
            }
        },
        'inr': {
            'code': 'inr',
            'minAmount': {
                'single': 145,
                'monthly': 145,
            },
            'symbol': '₹',
            'disabled': ['paypal', 'amex'],
            'monthlyUpgrade': [
                {'min': 20700, 'value': 2000},
                {'min': 13800, 'value': 1000},
                {'min': 6900, 'value': 700},
                {'min': 4830, 'value': 500},
                {'min': 2415, 'value': 350},
                {'min': 1035, 'value': 200},
            ],
            'presets': {
                'single': [1000, 500, 350, 200],
                'monthly': [650, 350, 200, 130]
            }
        },
        'jpy': {
            'code': 'jpy',
            'minAmount': {
                'single': 230,
                'monthly': 230,
            },
            'symbol': '¥',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 40,
                'micro': 7
            },
            'zeroDecimal': 'paypal',
            'monthlyUpgrade': [
                {'min': 32580, 'value': 3000},
                {'min': 21720, 'value': 2000},
                {'min': 10860, 'value': 1000},
                {'min': 7602, 'value': 750},
                {'min': 3801, 'value': 500},
                {'min': 1629, 'value': 300},
            ],
            'presets': {
                'single': [2240, 1120, 560, 340],
                'monthly': [1120, 560, 340, 230]
            }
        },
        'mxn': {
            'code': 'mxn',
            'minAmount': {
                'single': 40,
                'monthly': 40,
            },
            'symbol': '$',
            'paypalFixedFee': {
                'macro': 4.00,
                'micro': 0.55
            },
            'disabled': ['amex'],
            'monthlyUpgrade': [
                {'min': 5700, 'value': 500},
                {'min': 3800, 'value': 350},
                {'min': 1900, 'value': 200},
                {'min': 1330, 'value': 125},
                {'min': 665, 'value': 100},
                {'min': 285, 'value': 50},
            ],
            'presets': {
                'single': [400, 200, 100, 60],
                'monthly': [200, 100, 60, 40]
            }
        },
        'nok': {
            'code': 'nok',
            'minAmount': {
                'single': 17,
                'monthly': 17,
            },
            'symbol': 'kr',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 2.80,
                'micro': 0.47
            },
            'monthlyUpgrade': [
                {'min': 2598, 'value': 250},
                {'min': 1732, 'value': 175},
                {'min': 866, 'value': 80},
                {'min': 606, 'value': 60},
                {'min': 303, 'value': 40},
                {'min': 130, 'value': 25},
            ],
            'presets': {
                'single': [160, 80, 40, 20],
                'monthly': [100, 60, 30, 20]
            }
        },
        'nzd': {
            'code': 'nzd',
            'minAmount': {
                'single': 3,
                'monthly': 3,
            },
            'symbol': '$',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 0.45,
                'micro': 0.08
            },
            'monthlyUpgrade': [
                {'min': 450, 'value': 45},
                {'min': 300, 'value': 30},
                {'min': 150, 'value': 15},
                {'min': 105, 'value': 10},
                {'min': 52, 'value': 7},
                {'min': 23, 'value': 4},
            ],
            'presets': {
                'single': [10, 20, 30, 60],
                'monthly': [5, 10, 15, 20]
            }
        },
        'pln': {
            'code': 'pln',
            'minAmount': {
                'single': 7,
                'monthly': 7,
            },
            'symbol': 'zł',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 1.35,
                'micro': 0.23
            },
            'monthlyUpgrade': [
                {'min': 1146, 'value': 100},
                {'min': 764, 'value': 75},
                {'min': 382, 'value': 35},
                {'min': 267, 'value': 25},
                {'min': 134, 'value': 20},
                {'min': 57, 'value': 10},
            ],
            'presets': {
                'single': [80, 40, 20, 10],
                'monthly': [40, 20, 10, 7]
            }
        },
        'rub': {
            'code': 'rub',
            'minAmount': {
                'single': 130,
                'monthly': 130,
            },
            'symbol': '₽',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 10,
                'micro': 2
            },
            'monthlyUpgrade': [
                {'min': 18960, 'value': 2000},
                {'min': 12640, 'value': 1200},
                {'min': 6320, 'value': 600},
                {'min': 4424, 'value': 400},
                {'min': 2212, 'value': 300},
                {'min': 948, 'value': 200},
            ],
            'presets': {
                'single': [1300, 800, 500, 200],
                'monthly': [500, 300, 200, 130]
            }
        },
        'sek': {
            'code': 'sek',
            'minAmount': {
                'single': 18,
                'monthly': 18,
            },
            'symbol': 'kr',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 3.25,
                'micro': 0.54
            },
            'monthlyUpgrade': [
                {'min': 2832, 'value': 250},
                {'min': 1888, 'value': 175},
                {'min': 944, 'value': 90},
                {'min': 661, 'value': 65},
                {'min': 330, 'value': 50},
                {'min': 142, 'value': 25},
            ],
            'presets': {
                'single': [180, 90, 45, 30],
                'monthly': [90, 45, 30, 18]
            }
        },
        'twd': {
            'code': 'twd',
            'minAmount': {
                'single': 62,
                'monthly': 62,
            },
            'symbol': 'NT$',
            'disabled': ['amex'],
            'paypalFixedFee': {
                'macro': 10.00,
                'micro': 2.00
            },
            'zeroDecimal': 'paypal',
            'monthlyUpgrade': [
                {'min': 9300, 'value': 900},
                {'min': 6200, 'value': 600},
                {'min': 3100, 'value': 300},
                {'min': 2170, 'value': 200},
                {'min': 1085, 'value': 150},
                {'min': 465, 'value': 100},
            ],
            'presets': {
                'single': [480, 240, 150, 70],
                'monthly': [250, 150, 100, 62]
            }
        }
    }

    @classmethod
    def post_setup(cls):
        if env("SCOUT_KEY"):
            cls.SCOUT_MONITOR = True
            cls.SCOUT_KEY = env("SCOUT_KEY")
            cls.SCOUT_NAME = env("SCOUT_NAME", default="donate")

        logging.config.dictConfig(cls.LOGGING)

        # Set some fallbacks in django.conf.locale.LANG_INFO, and add some that don't exist
        django.conf.locale.LANG_INFO['ach'] = {
            'bidi': False,
            'code': 'ach',
            'name': 'Acholi',
            'name_local': 'Acholi',
        }
        django.conf.locale.LANG_INFO['en-US'] = {
            'bidi': False,
            'code': 'en-US',
            'name': 'English',
            'name_local': 'English (USA)',
        }
        django.conf.locale.LANG_INFO['en-AU'] = {
            'bidi': False,
            'code': 'en-AU',
            'name': 'English',
            'name_local': 'English (Australia)',
        }
        django.conf.locale.LANG_INFO['en-CA'] = {
            'bidi': False,
            'code': 'en-CA',
            'name': 'English',
            'name_local': 'English (Canada)',
        }
        django.conf.locale.LANG_INFO['en-GB'] = {
            'bidi': False,
            'code': 'en-GB',
            'name': 'English',
            'name_local': 'English (United Kingdom)',
        }
        django.conf.locale.LANG_INFO['en-IN'] = {
            'bidi': False,
            'code': 'en-IN',
            'name': 'English',
            'name_local': 'English (India)',
        }
        django.conf.locale.LANG_INFO['en-NZ'] = {
            'bidi': False,
            'code': 'en-NZ',
            'name': 'English',
            'name_local': 'English (New Zealand)',
        }
        django.conf.locale.LANG_INFO['es'] = {
            'bidi': False,
            'code': 'es',
            'name': 'Spain Spanish',
            'name_local': 'español (de España)'
        }
        django.conf.locale.LANG_INFO['es-MX'] = {
            'bidi': False,
            'code': 'es-MX',
            'name': 'Mexican Spanish',
            'name_local': 'español (de Mexico)',
            'fallback': ['es']
        }
        django.conf.locale.LANG_INFO['es-XL'] = {
            'bidi': False,
            'code': 'es-XL',
            'name': 'Latin American Spanish',
            'name_local': 'español (América Latina)',
            'fallback': ['es']
        }
        django.conf.locale.LANG_INFO['gu-IN'] = {
            'bidi': False,
            'code': 'gu-IN',
            'name': 'Gujarati',
            'name_local': 'ગુજરાતી',
        }
        django.conf.locale.LANG_INFO['lg'] = {
            'bidi': False,
            'code': 'lg',
            'name': 'Luganda',
            'name_local': 'Luganda',
        }
        django.conf.locale.LANG_INFO['lo'] = {
            'bidi': False,
            'code': 'lo',
            'name': 'Lao',
            'name_local': 'ລາວ',
        }
        django.conf.locale.LANG_INFO['pt-BR'] = {
            'bidi': False,
            'code': 'pt-BR',
            'name': 'Brazilian Portuguese',
            'name_local': 'português (do Brasil)',
        }
        django.conf.locale.LANG_INFO['pt-PT'] = {
            'bidi': False,
            'code': 'pt-PT',
            'name': 'European Portuguese',
            'name_local': 'português (Europeu)',
        }
        django.conf.locale.LANG_INFO['uk'] = {
            'bidi': False,
            'code': 'uk',
            'name': 'Ukrainian',
            'name_local': 'Українська',
        }
        django.conf.locale.LANG_INFO['uz'] = {
            'bidi': False,
            'code': 'uz',
            'name': 'Uzbek',
            'name_local': 'o‘zbek',
        }
        django.conf.locale.LANG_INFO['zh-CN'] = {
            'bidi': False,
            'code': 'zh-CN',
            'name': 'Chinese (China)',
            'name_local': '中文 (简体)',
        }
        django.conf.locale.LANG_INFO['zh-TW'] = {
            'bidi': False,
            'code': 'zh-TW',
            'name': 'Chinese (Taiwan)',
            'name_local': '正體中文 (繁體)',
        }
