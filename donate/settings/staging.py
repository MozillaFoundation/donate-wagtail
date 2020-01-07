from .environment import env
from .shared_settings import SharedSettingsDeployment
from .thunderbird import ThunderbirdOverrides


class Staging(SharedSettingsDeployment):
    DEBUG = False
    SECRET_KEY = env('DJANGO_SECRET_KEY')
    BASKET_API_ROOT_URL = env('BASKET_API_ROOT_URL')
    BASKET_SQS_QUEUE_URL = env('BASKET_SQS_QUEUE_URL')

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


class ThunderbirdStaging(Staging, ThunderbirdOverrides):
    INSTALLED_APPS = ThunderbirdOverrides.INSTALLED_APPS + Staging.INSTALLED_APPS

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
