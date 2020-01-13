from configurations import Configuration
from .environment import env
from .staging import Staging
from .secure import Secure
from .thunderbird import ThunderbirdOverrides


class ReviewApp(Staging, Configuration):
    ALLOWED_HOSTS = [f'{Secure.HEROKU_APP_NAME}.herokuapp.com']
    DEBUG = env('DEBUG')
    RECAPTCHA_ENABLED = False

    @classmethod
    def pre_setup(cls):
        super().pre_setup()

    @classmethod
    def setup(cls):
        super().setup()

    @classmethod
    def post_setup(cls):
        super().post_setup()


class ThunderbirdReviewApp(ReviewApp, ThunderbirdOverrides, Configuration):
    INSTALLED_APPS = ThunderbirdOverrides.INSTALLED_APPS + ReviewApp.INSTALLED_APPS

    @property
    def TEMPLATES(self):
        config = ReviewApp.TEMPLATES
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
