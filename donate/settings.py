"""
Django settings for donate project.
"""
import os
import environ
import logging.config

import django
import dj_database_url

app = environ.Path(__file__) - 1
root = app - 1

# We set defaults for values that aren't security related
# to the least permissive setting. For security related values,
# we rely on it being explicitly set (no default values) so that
# we error out first.
env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    ASSET_DOMAIN=(str, ''),
    AWS_LOCATION=(str, ''),
    AWS_ACCESS_KEY_ID=(str, ''),
    AWS_SECRET_ACCESS_KEY=(str, ''),
    AWS_REGION=(str, 'us-east-1'),
    CONTENT_TYPE_NO_SNIFF=bool,
    CORS_REGEX_WHITELIST=(tuple, ()),
    CORS_WHITELIST=(tuple, ()),
    DATABASE_URL=(str, None),
    DEBUG=(bool, False),
    DJANGO_LOG_LEVEL=(str, 'INFO'),
    HEROKU_APP_NAME=(str, ''),
    SET_HSTS=bool,
    SSL_REDIRECT=bool,
    USE_S3=(bool, True),
    USE_X_FORWARDED_HOST=(bool, False),
    XSS_PROTECTION=bool,
    REDIS_URL=(str, ''),
    RANDOM_SEED=(int, None),
    # Braintree
    BRAINTREE_USE_SANDBOX=(bool, True),
    BRAINTREE_MERCHANT_ID=(str, ''),
    BRAINTREE_PUBLIC_KEY=(str, ''),
    BRAINTREE_PRIVATE_KEY=(str, ''),
    BRAINTREE_TOKENIZATION_KEY=(str, ''),
    BRAINTREE_MERCHANT_ACCOUNTS=(dict, {}),
    BRAINTREE_PLANS=(dict, {}),
    # Basket and SQS
    BASKET_API_ROOT_URL=(str, ''),
    BASKET_SQS_QUEUE_URL=(str, ''),
    # Pontoon
    WAGTAILLOCALIZE_PONTOON_GIT_URL=(str, ''),
    WAGTAILLOCALIZE_PONTOON_GIT_CLONE_DIR=(str, ''),
    # Recaptcha
    RECAPTCHA_SITE_KEY=(str, ''),
    RECAPTCHA_SECRET_KEY=(str, ''),
    RECAPTCHA_ENABLED=(bool, False),
)

# Read in the environment
if os.path.exists(f'{root}/.env') is True:
    environ.Env.read_env(f'{root}/.env')
else:
    environ.Env.read_env()


SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS
USE_X_FORWARDED_HOST = env('USE_X_FORWARDED_HOST')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

HEROKU_APP_NAME = env('HEROKU_APP_NAME')

if HEROKU_APP_NAME:
    ALLOWED_HOSTS.append(HEROKU_APP_NAME + '.herokuapp.com')

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
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]

MIDDLEWARE = [
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
]

ROOT_URLCONF = 'donate.urls'

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

WSGI_APPLICATION = 'donate.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('db.sqlite3'),
    }
}

DATABASE_URL = env('DATABASE_URL')

if DATABASE_URL is not None:
    DATABASES['default'].update(dj_database_url.config())

DATABASES['default']['ATOMIC_REQUESTS'] = True

if env('REDIS_URL'):
    REDIS_URL = env('REDIS_URL')

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                # timeout for read/write operations after a connection is established
                'SOCKET_TIMEOUT': 120,
                # timeout for the connection to be established
                'SOCKET_CONNECT_TIMEOUT': 30,
                # Enable compression
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
                # Ignore exceptions, redis only used for caching (i.e. if redis fails, will use database)
                'IGNORE_EXCEPTIONS': True
            }
        }
    }
else:
    REDIS_URL = None

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-US'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    app('locale'),
]

LANGUAGES = [
    ('ach', 'Acholi'),
    ('ar', 'Arabic'),
    ('ast', 'Asturian'),
    ('az', 'Azerbaijani'),
    ('bn', 'Bengali'),
    ('bs', 'Bosnian'),
    ('ca', 'Catalan'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('de', 'German'),
    ('dsb', 'Sorbian, Lower'),
    ('el', 'Greek'),
    ('en-US', 'English (US)'),
    ('en-CA', 'English (Canada)'),
    ('en-GB', 'English (Great Britain)'),
    ('es', 'Spanish'),
    ('es-AR', 'Spanish (Argentina)'),
    ('es-CL', 'Spanish (Chile)'),
    ('es-MX', 'Spanish (Mexico)'),
    ('es-XL', 'Spanish (Latin America)'),
    ('et', 'Estonian'),
    ('fr', 'French'),
    ('fy-NL', 'Frisian'),
    ('gu-IN', 'Gujarati'),
    ('he', 'Hebrew'),
    ('hi-IN', 'Hindi'),
    ('hr', 'Croatian'),
    ('hsb', 'Sorbian, Upper'),
    ('hu', 'Hungarian'),
    ('id', 'Indonesian'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('ka', 'Georgian'),
    ('kab', 'Kabyle'),
    ('ko', 'Korean'),
    ('lg', 'Luganda'),
    ('lo', 'Lao'),
    ('lv', 'Latvian'),
    ('lg', 'Luganda'),
    ('ms', 'Malay'),
    ('ml', 'Malayalam'),
    ('mr', 'Marathi'),
    ('nb-NO', 'Norwegian Bokmål'),
    ('nl', 'Dutch'),
    ('nn-NO', 'Norwegian Nynorsk'),
    ('pl', 'Polish'),
    ('pt-BR', 'Portuguese (Brazil)'),
    ('pt-PT', 'Portuguese (Portugal)'),
    ('pa-IN', 'Punjabi'),
    ('ro', 'Romanian'),
    ('ru', 'Russian'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('sq', 'Albanian'),
    ('sv-SE', 'Swedish'),
    ('ta', 'Tamil'),
    ('te', 'Telugu'),
    ('th', 'Thai'),
    ('tr', 'Turkish'),
    ('uk', 'Ukrainian'),
    ('uz', 'Uzbek'),
    ('zh-CN', 'Chinese (China)'),
    ('zh-TW', 'Chinese (Taiwan)'),
]

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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [app('frontend')]
STATIC_ROOT = root('static')
STATIC_URL = '/static/'

# S3 credentials for SQS and S3
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_LOCATION = env('AWS_LOCATION')
AWS_REGION = env('AWS_REGION')

# Storage for user generated files
USE_S3 = env('USE_S3')
if USE_S3:
    # Use S3 to store user files if the corresponding environment var is set
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
    MEDIA_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/'
    MEDIA_ROOT = ''
    # This is a workaround for https://github.com/wagtail/wagtail/issues/3206
    AWS_S3_FILE_OVERWRITE = False
else:
    # Otherwise use the default filesystem storage
    MEDIA_ROOT = root('media/')
    MEDIA_URL = '/media/'


# Remove the default Django loggers and configure new ones
LOGGING_CONFIG = None
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
            'handlers': ['info'],
            'level': 'INFO',
        },
        'donate': {
            'handlers': ['info'],
            'level': 'INFO',
        }
    }
}
DJANGO_LOG_LEVEL = env('DJANGO_LOG_LEVEL')
logging.config.dictConfig(LOGGING)

# CSP
CSP_DEFAULT = (
    '\'self\''
)

CSP_DEFAULT_SRC = env('CSP_DEFAULT_SRC', default=CSP_DEFAULT)
CSP_SCRIPT_SRC = env('CSP_SCRIPT_SRC', default=CSP_DEFAULT)
CSP_IMG_SRC = env('CSP_IMG_SRC', default=CSP_DEFAULT)
CSP_OBJECT_SRC = env('CSP_OBJECT_SRC', default=None)
CSP_MEDIA_SRC = env('CSP_MEDIA_SRC', default=None)
CSP_FRAME_SRC = env('CSP_FRAME_SRC', default=None)
CSP_FONT_SRC = env('CSP_FONT_SRC', default=CSP_DEFAULT)
CSP_CONNECT_SRC = env('CSP_CONNECT_SRC', default=None)
CSP_STYLE_SRC = env('CSP_STYLE_SRC', default=CSP_DEFAULT)
CSP_BASE_URI = env('CSP_BASE_URI', default=None)
CSP_CHILD_SRC = env('CSP_CHILD_SRC', default=None)
CSP_FRAME_ANCESTORS = env('CSP_FRAME_ANCESTORS', default=None)
CSP_FORM_ACTION = env('CSP_FORM_ACTION', default=None)
CSP_SANDBOX = env('CSP_SANDBOX', default=None)
CSP_REPORT_URI = env('CSP_REPORT_URI', default=None)
CSP_WORKER_SRC = env('CSP_WORKER_SRC', default=CSP_DEFAULT)

# Security
SECURE_BROWSER_XSS_FILTER = env('XSS_PROTECTION')
SECURE_CONTENT_TYPE_NOSNIFF = env('CONTENT_TYPE_NO_SNIFF')
SECURE_HSTS_INCLUDE_SUBDOMAINS = env('SET_HSTS')
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 31 * 6
SECURE_SSL_REDIRECT = env('SSL_REDIRECT')
# Heroku goes into an infinite redirect loop without this.
# See https://docs.djangoproject.com/en/1.10/ref/settings/#secure-ssl-redirect
if env('SSL_REDIRECT') is True:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')
REFERRER_POLICY = 'no-referrer-when-downgrade'

AUTH_USER_MODEL = 'users.User'

RANDOM_SEED = env('RANDOM_SEED')

# Braintree
BRAINTREE_USE_SANDBOX = env('BRAINTREE_USE_SANDBOX')
BRAINTREE_MERCHANT_ID = env('BRAINTREE_MERCHANT_ID')
BRAINTREE_PUBLIC_KEY = env('BRAINTREE_PUBLIC_KEY')
BRAINTREE_PRIVATE_KEY = env('BRAINTREE_PRIVATE_KEY')
BRAINTREE_TOKENIZATION_KEY = env('BRAINTREE_TOKENIZATION_KEY')
BRAINTREE_MERCHANT_ACCOUNTS = env('BRAINTREE_MERCHANT_ACCOUNTS')
BRAINTREE_PLANS = env('BRAINTREE_PLANS')

BRAINTREE_PARAMS = {
    'use_sandbox': BRAINTREE_USE_SANDBOX,
    'token': BRAINTREE_TOKENIZATION_KEY,
}

# Basket
BASKET_API_ROOT_URL = env('BASKET_API_ROOT_URL') or None
BASKET_SQS_QUEUE_URL = env('BASKET_SQS_QUEUE_URL') or None

# Pontoon settings
WAGTAILLOCALIZE_PONTOON_SYNC_MANAGER_CLASS = 'donate.core.pontoon.CustomSyncManager'
WAGTAILLOCALIZE_PONTOON_GIT_URL = env('WAGTAILLOCALIZE_PONTOON_GIT_URL')
WAGTAILLOCALIZE_PONTOON_GIT_CLONE_DIR = env('WAGTAILLOCALIZE_PONTOON_GIT_CLONE_DIR')

# Recaptcha
RECAPTCHA_SITE_KEY = env('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = env('RECAPTCHA_SECRET_KEY')
RECAPTCHA_ENABLED = env('RECAPTCHA_ENABLED')

# Django-rq
RQ_QUEUES = {
    'default': {
        'URL': REDIS_URL or 'redis://localhost:6379/0',
        'DEFAULT_TIMEOUT': 500,
    },

    # Must be a separate queue as it's limited to one item at a time
    'wagtail_localize_pontoon.sync': {
        'URL': REDIS_URL or 'redis://localhost:6379/0',
        'DEFAULT_TIMEOUT': 500,
    },
}

# Wagtail settings

# This name is displayed in the Wagtail admin.
WAGTAIL_SITE_NAME = "donate"
