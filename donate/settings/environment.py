import os
import environ

from . import defaults

# We set defaults for values that aren't security related
# to the least permissive setting. For security related values,
# we rely on it being explicitly set (no default values) so that
# we error out first.
env = environ.Env(
    ACOUSTIC_TX_CLIENT_ID=(str, ''),
    ACOUSTIC_TX_CLIENT_SECRET=(str, ''),
    ACOUSTIC_TX_REFRESH_TOKEN=(str, ''),
    ACOUSTIC_TX_SERVER_NUMBER=(str, ''),
    ALLOWED_HOSTS=(list, '*'),
    AUTO_CLOSE_STRIPE_DISPUTES=(bool, False),
    AWS_ACCESS_KEY_ID=(str, ''),
    AWS_LOCATION=(str, ''),
    AWS_REGION=(str, ''),
    AWS_S3_CUSTOM_DOMAIN=(str, ''),
    AWS_SECRET_ACCESS_KEY=(str, ''),
    AWS_STORAGE_BUCKET_NAME=(str, ''),
    BASKET_API_ROOT_URL=(str, ''),
    BASKET_SQS_QUEUE_URL=(str, ''),
    BASKET_URL=(str, ''),
    BRAINTREE_MERCHANT_ACCOUNTS=(dict, defaults.BRAINTREE_MERCHANT_ACCOUNTS),
    BRAINTREE_MERCHANT_ACCOUNTS_PAYPAL_MICRO=(dict, {}),
    BRAINTREE_MERCHANT_ID=(str, 'test'),
    BRAINTREE_PLANS=(dict, defaults.BRAINTREE_PLANS),
    BRAINTREE_PRIVATE_KEY=(str, 'test'),
    BRAINTREE_PUBLIC_KEY=(str, 'test'),
    BRAINTREE_TOKENIZATION_KEY=(str, ''),
    BRAINTREE_USE_SANDBOX=(bool, True),
    CSP_BASE_URI=(tuple, defaults.CSP_BASE_URI),
    CSP_CONNECT_SRC=(tuple, defaults.CSP_CONNECT_SRC),
    CSP_DEFAULT_SRC=(tuple, defaults.CSP_DEFAULT_SRC),
    CSP_FONT_SRC=(tuple, defaults.CSP_FONT_SRC),
    CSP_FORM_ACTION=(tuple, defaults.CSP_DEFAULT_SRC),
    CSP_FRAME_ANCESTORS=(tuple, defaults.CSP_DEFAULT_SRC),
    CSP_FRAME_SRC=(tuple, defaults.CSP_FRAME_SRC),
    CSP_IMG_SRC=(tuple, defaults.CSP_IMG_SRC),
    CSP_MEDIA_SRC=(tuple, defaults.CSP_DEFAULT_SRC),
    CSP_OBJECT_SRC=(tuple, defaults.CSP_DEFAULT_SRC),
    CSP_REPORT_URI=(tuple, None),
    CSP_SCRIPT_SRC=(tuple, defaults.CSP_SCRIPT_SRC),
    CSP_STYLE_SRC=(tuple, defaults.CSP_STYLE_SRC),
    CSP_WORKER_SRC=(tuple, defaults.CSP_WORKER_SRC),
    DATABASE_URL=(str, 'postgres://donate:mozilla@postgres:5432/donate'),
    DEBUG=(bool, False),
    DJANGO_LOG_LEVEL=(str, 'INFO'),
    DJANGO_SECRET_KEY=(str, None),
    DOMAIN_REDIRECT_MIDDLEWARE_ENABLED=(bool, False),
    DONATION_RECEIPT_METHOD=(str, 'BASKET'),
    ENABLE_THUNDERBIRD_REDIRECT=(bool, False),
    GITHUB_TOKEN=(str, ''),
    HEROKU_PR_NUMBER=(str, ''),
    HEROKU_BRANCH=(str, ''),
    HEROKU_APP_NAME=(str, ''),
    HEROKU_RELEASE_VERSION=(str, 'Development'),
    MIGRATE_STRIPE_SUBSCRIPTIONS_ENABLED=(bool, False),
    POST_DONATE_NEWSLETTER_URL=(str, None),
    RANDOM_SEED=(int, None),
    RECAPTCHA_ENABLED=(bool, False),
    RECAPTCHA_SECRET_KEY=(str, ''),
    RECAPTCHA_SITE_KEY=(str, ''),
    REDIS_URL=(str, 'redis://redis:6397/0'),
    REVIEW_APP=(bool, False),
    SALESFORCE_ORGID=(str, ''),
    SALESFORCE_CASE_RECORD_TYPE_ID=(str, ''),
    SENTRY_DSN=(str, None),
    SENTRY_ENVIRONMENT=(str, None),
    SET_HSTS=(bool, False),
    SLACK_WEBHOOK_RA=(str, ''),
    SLACK_WEBHOOK_PONTOON=(str, ''),
    SSH_KEY=(str, None),
    SSH_CONFIG=(str, None),
    SSL_REDIRECT=(bool, False),
    STRIPE_API_KEY=(str, ''),
    STRIPE_WEBHOOK_SECRET=(str, ''),
    TARGET_DOMAINS=(list, []),
    TRAVIS_LOGS_URL=(str, ''),
    USE_S3=(bool, False),
    WAGTAILLOCALIZE_PONTOON_GIT_CLONE_DIR=(str, ''),
    WAGTAILLOCALIZE_PONTOON_GIT_URL=(str, ''),
    # Mozilla OIDC
    USE_CONVENTIONAL_AUTH=(bool, True),
    OIDC_RP_CLIENT_ID=(str, None),
    OIDC_RP_CLIENT_SECRET=(str, None),
    OIDC_OP_AUTHORIZATION_ENDPOINT=(str, "https://auth.mozilla.auth0.com/authorize"),
    OIDC_OP_TOKEN_ENDPOINT=(str, "https://auth.mozilla.auth0.com/oauth/token"),
    OIDC_OP_USER_ENDPOINT=(str, "https://auth.mozilla.auth0.com/userinfo"),
    OIDC_OP_DOMAIN=(str, "auth.mozilla.auth0.com"),
    OIDC_OP_JWKS_ENDPOINT=(str, "https://auth.mozilla.auth0.com/.well-known/jwks.json"),
    SCOUT_KEY=(str, None),
)


app = environ.Path(__file__) - 2
root = app - 1

# Read in the environment
if os.path.exists(f'{root}/.env') is True:
    environ.Env.read_env(f'{root}/.env')
else:
    environ.Env.read_env()
