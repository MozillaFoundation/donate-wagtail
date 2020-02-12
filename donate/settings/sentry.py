from .environment import env


class Sentry(object):
    SENTRY_DSN = env('SENTRY_DSN')
    SENTRY_ENVIRONMENT = env('SENTRY_ENVIRONMENT')
    HEROKU_RELEASE_VERSION = env('HEROKU_RELEASE_VERSION')

    @classmethod
    def pre_setup(cls):
        super().pre_setup()

        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        sentry_sdk.init(
            dsn=cls.SENTRY_DSN,
            integrations=[DjangoIntegration()],
            release=cls.HEROKU_RELEASE_VERSION,
            environment=cls.SENTRY_ENVIRONMENT
        )
