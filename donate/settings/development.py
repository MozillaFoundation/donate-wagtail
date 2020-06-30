from configurations import Configuration
from .environment import env
from .secure import Secure
from .oidc import OIDC
from .database import Database
from .base import Base
from .redis import Redis
from .braintree import Braintree
from .s3 import S3
from .salesforce import Salesforce
from .thunderbird import ThunderbirdOverrides


class Development(Base, Secure, OIDC, Database, Redis, S3, Salesforce, Braintree, Configuration):
    DEBUG = env('DEBUG')
    DJANGO_LOG_LEVEL = env('DJANGO_LOG_LEVEL')

    RECAPTCHA_ENABLED = False
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    USE_X_FORWARDED_HOST = False
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False

    # In dev, lets not worry about enforcing password changes
    AUTH_PASSWORD_VALIDATORS = []

    @classmethod
    def pre_setup(cls):
        super().pre_setup()

    @classmethod
    def setup(cls):
        super().setup()

    @classmethod
    def post_setup(cls):
        super().post_setup()


class ThunderbirdDevelopment(Development, ThunderbirdOverrides, Configuration):
    INSTALLED_APPS = ThunderbirdOverrides.INSTALLED_APPS + Development.INSTALLED_APPS
    FRONTEND = ThunderbirdOverrides.FRONTEND
    ENABLE_THUNDERBIRD_REDIRECT = False
    FRAUD_SITE_ID = 'tbird'

    @property
    def TEMPLATES(self):
        config = Development.TEMPLATES
        config[0]['DIRS'] = ThunderbirdOverrides.TEMPLATES_DIR + config[0]['DIRS']
        return config

    @classmethod
    def pre_setup(cls):
        super().pre_setup()

    @classmethod
    def setup(cls):
        super().setup()

    @classmethod
    def post_setup(cls):
        super().post_setup()
