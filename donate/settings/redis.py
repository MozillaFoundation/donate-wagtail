from .environment import env


class Redis(object):
    REDIS_URL = env('REDIS_URL')
    REDIS_QUEUE_URL = env('REDIS_QUEUE_URL', default=REDIS_URL)

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'SOCKET_TIMEOUT': 120,
                'SOCKET_CONNECT_TIMEOUT': 30,
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
                'IGNORE_EXCEPTIONS': True
            }
        }
    }

    RQ_QUEUES = {
        'default': {
            'URL': REDIS_QUEUE_URL,
            'DEFAULT_TIMEOUT': 500
        },
        # Must be a separate queue as it's limited to one item at a time
        'wagtail_localize_pontoon.sync': {
            'URL': REDIS_QUEUE_URL,
            'DEFAULT_TIMEOUT': 500
        }
    }
