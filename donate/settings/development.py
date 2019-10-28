from configurations import Configuration
from .environment import env
from .database import Database
from .base import Base
from .redis import Redis
from .braintree import Braintree
from .s3 import S3
from .thunderbird import ThunderbirdOverrides


class Development(Base, Database, Redis, S3, Braintree, Configuration):
    DEBUG = env('DEBUG')
    DJANGO_LOG_LEVEL = env('DJANGO_LOG_LEVEL')

    SECRET_KEY = env('DJANGO_SECRET_KEY')
    ALLOWED_HOSTS = env('ALLOWED_HOSTS')

    CONTENT_TYPE_NO_SNIFF = env('CONTENT_TYPE_NO_SNIFF')
    SSL_REDIRECT = env('SSL_REDIRECT')
    USE_X_FORWARDED_FOR = env('USE_X_FORWARDED_FOR')
    X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')
    XSS_PROTECTION = env('XSS_PROTECTION')
    CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE')
    SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE')

    # In dev, lets not worry about enforcing password changes
    AUTH_PASSWORD_VALIDATORS = env('AUTH_PASSWORD_VALIDATORS')

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
