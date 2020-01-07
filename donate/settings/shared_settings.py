from configurations import Configuration
from .base import Base
from .oidc import OIDC
from .database import Database
from .redis import Redis
from .s3 import S3
from .secure import Secure
from .sentry import Sentry
from .braintree import Braintree

class SharedSettings(Base, OIDC, Database, Redis, S3, Braintree, Configuration):
    @classmethod
    def pre_setup(cls):
        super().pre_setup()

    @classmethod
    def setup(cls):
        super().setup()

    @classmethod
    def post_setup(cls):
        super().post_setup()


class SharedSettingsDeployment(Secure, Sentry, SharedSettings):
    @classmethod
    def pre_setup(cls):
        super().pre_setup()

    @classmethod
    def setup(cls):
        super().setup()

    @classmethod
    def post_setup(cls):
        super().post_setup()
