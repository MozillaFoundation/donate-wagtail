import django
import logging.config

from . import defaults
from .environment import (
    env,
    app,
    root
)

from .languages import LANGUAGES


class Base(object):
    SECRET_KEY = 'CHANGE ME OUTSIDE OF DEV'
    WAGTAIL_SITE_NAME = 'donate'
    WSGI_APPLICATION = 'donate.wsgi.application'
    RECAPTCHA_ENABLED = False
    LANGUAGE_CODE = 'en-US'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    AUTH_USER_MODEL = 'users.User'
    DJANGO_LOG_LEVEL = env('DJANGO_LOG_LEVEL')
    ALLOWED_HOSTS = env('ALLOWED_HOSTS')
    RANDOM_SEED = env('RANDOM_SEED')

    # Domain Redirects
    DOMAIN_REDIRECT_MIDDLEWARE_ENABLED = env('DOMAIN_REDIRECT_MIDDLEWARE_ENABLED')
    TARGET_DOMAINS = env('TARGET_DOMAINS')

    # Initialize these attributes to None
    BASKET_API_ROOT_URL = env('BASKET_API_ROOT_URL')
    BASKET_SQS_QUEUE_URL = env('BASKET_SQS_QUEUE_URL')

    # Pontoon settings
    WAGTAILLOCALIZE_PONTOON_SYNC_MANAGER_CLASS = 'donate.core.pontoon.CustomSyncManager'
    WAGTAILLOCALIZE_PONTOON_GIT_URL = env('WAGTAILLOCALIZE_PONTOON_GIT_URL')
    WAGTAILLOCALIZE_PONTOON_GIT_CLONE_DIR = env('WAGTAILLOCALIZE_PONTOON_GIT_CLONE_DIR')

    # Static content settings
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATICFILES_DIRS = [app('frontend')]
    STATIC_ROOT = root('static')
    STATIC_URL = '/static/'

    MEDIA_ROOT = root('media/')
    MEDIA_URL = '/media/'

    # Stripe
    STRIPE_API_KEY = env('STRIPE_API_KEY')
    STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET')

    LOCALE_PATHS = [
        app('locale'),
    ]

    # Review apps' slack bot
    GITHUB_TOKEN = env('GITHUB_TOKEN')
    SLACK_WEBHOOK_RA = env('SLACK_WEBHOOK_RA')

    # Pontoon check slack bot
    SLACK_WEBHOOK_PONTOON = env('SLACK_WEBHOOK_PONTOON')
    TRAVIS_LOGS_URL = env('TRAVIS_JOB_WEB_URL', default='')

    @property
    def CSRF_TRUSTED_ORIGINS(self):
        return self.ALLOWED_HOSTS

    INSTALLED_APPS = [
        'donate.users',
        'donate.core',
        'donate.payments',
        'donate.recaptcha',

        'wagtail_localize',
        'wagtail_localize.admin.language_switch',
        'wagtail_localize.translation_memory',
        'wagtail_localize_pontoon',

        'wagtail.contrib.settings',
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
            'wagtail.core.middleware.SiteMiddleware',
            'csp.middleware.CSPMiddleware',
            # Make sure to check for deauthentication during a session:
            'mozilla_django_oidc.middleware.SessionRefresh'
        ]))

    ROOT_URLCONF = 'donate.urls'

    TEMPLATES = defaults.TEMPLATES

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': root('db.sqlite3'),
        }
    }

    RQ_QUEUES = defaults.RQ_QUEUES

    LANGUAGES = LANGUAGES

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

    @classmethod
    def post_setup(cls):
        logging.config.dictConfig(cls.LOGGING)

        # Set some fallbacks in django.conf.locale.LANG_INFO, and add some that don't exist
        django.conf.locale.LANG_INFO['es-ar']['fallback'] = ['es']
        django.conf.locale.LANG_INFO['es-mx']['fallback'] = ['es']
        django.conf.locale.LANG_INFO['es-cl'] = {
            'bidi': False,
            'code': 'es-cl',
            'name': 'Chilean Spanish',
            'name_local': 'español de Chile',
            'fallback': ['es']
        }
        django.conf.locale.LANG_INFO['es-xl'] = {
            'bidi': False,
            'code': 'es-xl',
            'name': 'Latin American Spanish',
            'name_local': 'español',
            'fallback': ['es']
        }
        django.conf.locale.LANG_INFO['ach'] = {
            'bidi': False,
            'code': 'ach',
            'name': 'Acholi',
            'name_local': 'Acholi',
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
            'name_local': 'Lao',
        }
        django.conf.locale.LANG_INFO['ms'] = {
            'bidi': False,
            'code': 'ms',
            'name': 'Malay',
            'name_local': 'Malay',
        }
        django.conf.locale.LANG_INFO['uk'] = {
            'bidi': False,
            'code': 'uk',
            'name': 'Ukrainian',
            'name_local': 'Ukrainian',
        }
