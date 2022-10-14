from .environment import env


class Secure(object):
    USE_X_FORWARDED_HOST = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31556952
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    X_FRAME_OPTIONS = 'DENY'
    REFERRER_POLICY = 'no-referrer-when-downgrade'

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Recaptcha
    USE_RECAPTCHA = True
    RECAPTCHA_SITE_KEY = env('RECAPTCHA_SITE_KEY')
    RECAPTCHA_SECRET_KEY = env('RECAPTCHA_SECRET_KEY')
    RECAPTCHA_SITE_KEY_CHECKBOX = env('RECAPTCHA_SITE_KEY_CHECKBOX')
    RECAPTCHA_SECRET_KEY_CHECKBOX = env('RECAPTCHA_SECRET_KEY_CHECKBOX')
    RECAPTCHA_SITE_KEY_REGULAR = env('RECAPTCHA_SITE_KEY_REGULAR')
    USE_CHECKBOX_RECAPTCHA_FOR_CC = env('USE_CHECKBOX_RECAPTCHA_FOR_CC')

    HEROKU_APP_NAME = env('HEROKU_APP_NAME')
