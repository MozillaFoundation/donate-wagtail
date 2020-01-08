from configurations import Configuration
from .environment import env
from .staging import Staging
from .secure import Secure


class ReviewApp(Staging, Configuration):
    ALLOWED_HOSTS = [f'{Secure.HEROKU_APP_NAME}.herokuapp.com']
    DEBUG = env('DEBUG')

    @classmethod
    def pre_setup(cls):
        super().pre_setup()

    @classmethod
    def setup(cls):
        super().setup()

    @classmethod
    def post_setup(cls):
        super().post_setup()
