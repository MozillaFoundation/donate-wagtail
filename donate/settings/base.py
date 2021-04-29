import django
import logging.config
import sys
from . import defaults
from .environment import (
    env,
    app,
    root
)

from .languages import LANGUAGES


class Base(object):
    SECRET_KEY = env('DJANGO_SECRET_KEY')
    WAGTAIL_SITE_NAME = 'donate'
    WSGI_APPLICATION = 'donate.wsgi.application'
    LANGUAGE_CODE = 'en-US'
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

    # Override URL for posting newsletter subscriptions
    POST_DONATE_NEWSLETTER_URL = env('POST_DONATE_NEWSLETTER_URL')

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
            'donate.utility.middleware.TargetDomainRedirectMiddleware'
            if self.DOMAIN_REDIRECT_MIDDLEWARE_ENABLED else None,
            'django.middleware.gzip.GZipMiddleware',
            'django.middleware.security.SecurityMiddleware',
            'whitenoise.middleware.WhiteNoiseMiddleware',
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

    FRONTEND = {
        'RELEASE_VERSION': env('HEROKU_RELEASE_VERSION'),
        'SENTRY_DSN': env('SENTRY_DSN'),
        'SENTRY_ENVIRONMENT': env('SENTRY_ENVIRONMENT'),
        'BRAINTREE_MERCHANT_ACCOUNTS': env('BRAINTREE_MERCHANT_ACCOUNTS'),
        'PAYPAL_DISPLAY_NAME': 'Mozilla Foundation'
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
