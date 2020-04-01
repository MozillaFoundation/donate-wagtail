from .environment import app, env


class ThunderbirdOverrides(object):
    INSTALLED_APPS = ['donate.thunderbird']
    TEMPLATES_DIR = [app('thunderbird/templates')]
    FRONTEND = {
        'RELEASE_VERSION': env('HEROKU_RELEASE_VERSION'),
        'SENTRY_DSN': env('SENTRY_DSN'),
        'SENTRY_ENVIRONMENT': env('SENTRY_ENVIRONMENT'),
        'BRAINTREE_MERCHANT_ACCOUNTS': env('BRAINTREE_MERCHANT_ACCOUNTS'),
        'PAYPAL_DISPLAY_NAME': 'MZLA Technologies'
    }
