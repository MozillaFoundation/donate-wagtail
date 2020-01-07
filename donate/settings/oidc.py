from .environment import env


# Mozilla OpenID Connect/Auth0 configuration
class OIDC(object):
    # disable user creating during authentication
    OIDC_CREATE_USER = False

    # How frequently do we check with the provider that the user still exists.
    OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 15 * 60

    OIDC_RP_SIGN_ALGO = "RS256"
    OIDC_RP_CLIENT_ID = env("OIDC_RP_CLIENT_ID")
    OIDC_RP_CLIENT_SECRET = env("OIDC_RP_CLIENT_SECRET")

    # These values should be overwritten by thunderbird/other instances:
    OIDC_OP_AUTHORIZATION_ENDPOINT = "https://auth.mozilla.auth0.com/authorize"
    OIDC_OP_TOKEN_ENDPOINT = "https://auth.mozilla.auth0.com/oauth/token"
    OIDC_OP_USER_ENDPOINT = "https://auth.mozilla.auth0.com/userinfo"
    OIDC_OP_DOMAIN = "auth.mozilla.auth0.com"
    OIDC_OP_JWKS_ENDPOINT = "https://auth.mozilla.auth0.com/.well-known/jwks.json"

    LOGIN_REDIRECT_URL = "/admin/"
    LOGOUT_REDIRECT_URL = "/"

    # If True (which should only be done in settings.local), then show username and
    # password fields. You'll also need to enable the model backend in local settings
    USE_CONVENTIONAL_AUTH = env('USE_CONVENTIONAL_AUTH')

    # Extra Wagtail config to disable password usage (SSO should be the only way in)
    # https://docs.wagtail.io/en/v2.6.3/advanced_topics/settings.html#password-management
    # Don't let users change or reset their password
    WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = False
    WAGTAIL_PASSWORD_RESET_ENABLED = False

    # Don't require a password when creating a user,
    # and blank password means cannot log in unless SSO
    WAGTAILUSERS_PASSWORD_ENABLED = False

    @classmethod
    def setup(cls):
        # EXTRA LOGGING
        cls.LOGGING['loggers']['mozilla_django_oidc'] = {
            'handlers': ['debug'],
            'level': 'INFO',
        }

        if cls.USE_CONVENTIONAL_AUTH is False:
            cls.AUTHENTICATION_BACKENDS = (
                'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
            )
