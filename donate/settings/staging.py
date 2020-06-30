from configurations import Configuration
from .base import Base
from .secure import Secure
from .oidc import OIDC
from .database import Database
from .redis import Redis
from .s3 import S3
from .salesforce import Salesforce
from .braintree import Braintree
from .sentry import Sentry
from .thunderbird import ThunderbirdOverrides


class Staging(Base, Secure, OIDC, Database, Redis, S3, Salesforce, Braintree, Sentry, Configuration):
    DEBUG = False

    @classmethod
    def pre_setup(cls):
        super().pre_setup()
        cls.LOGGING['loggers']['rq.worker']['handlers'] = ['info']
        cls.LOGGING['loggers']['rq.worker']['level'] = 'INFO'

    @classmethod
    def setup(cls):
        super().setup()

    @classmethod
    def post_setup(cls):
        super().post_setup()


class ThunderbirdStaging(Staging, ThunderbirdOverrides, Configuration):
    INSTALLED_APPS = ThunderbirdOverrides.INSTALLED_APPS + Staging.INSTALLED_APPS
    FRONTEND = ThunderbirdOverrides.FRONTEND
    ENABLE_THUNDERBIRD_REDIRECT = False
    FRAUD_SITE_ID = 'tbird'

    @property
    def TEMPLATES(self):
        config = Staging.TEMPLATES
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
