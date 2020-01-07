from .environment import env
from .shared_settings import SharedSettingsDeployment
from .thunderbird import ThunderbirdOverrides


class Production(SharedSettingsDeployment):
    DEBUG = False
    SECRET_KEY = env('DJANGO_SECRET_KEY')
    BASKET_API_ROOT_URL = env('BASKET_API_ROOT_URL')
    BASKET_SQS_QUEUE_URL = env('BASKET_SQS_QUEUE_URL')
    SSH_KEY = env('SSH_KEY')
    SSH_CONFIG = env('SSH_CONFIG')

    @classmethod
    def pre_setup(cls):
        super().pre_setup()
        # production forces debug to be False, so the rq worker will never log donor data with the config below.
        cls.LOGGING['loggers']['rq.worker']['handlers'] = ['DEBUG']
        cls.LOGGING['loggers']['rq.worker']['level'] = 'DEBUG'

    @classmethod
    def setup(cls):
        super().setup()

    @classmethod
    def post_setup(cls):
        super().post_setup()


class ThunderbirdProduction(Production, ThunderbirdOverrides):
    INSTALLED_APPS = ThunderbirdOverrides.INSTALLED_APPS + Production.INSTALLED_APPS

    @property
    def TEMPLATES(self):
        config = Production.TEMPLATES
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
