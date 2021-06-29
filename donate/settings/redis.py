from .environment import env


class Redis(object):
    REDIS_URL = env('REDIS_URL')
    REDIS_QUEUE_URL = env('REDIS_QUEUE_URL', default=REDIS_URL)

    connection_pool_kwargs = {}

    if REDIS_URL.startswith("rediss"):
        connection_pool_kwargs["ssl_cert_reqs"] = None

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'SOCKET_TIMEOUT': 120,
                'SOCKET_CONNECT_TIMEOUT': 30,
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
                'IGNORE_EXCEPTIONS': True,
                "CONNECTION_POOL_KWARGS": connection_pool_kwargs
            }
        }
    }

    RQ_QUEUES = {
        'default': {
            'URL': REDIS_QUEUE_URL,
            'DEFAULT_TIMEOUT': 500,
            'SSL_CERT_REQS': None
        },
        # Must be a separate queue as it's limited to one item at a time
        'wagtail_localize_pontoon.sync': {
            'URL': REDIS_QUEUE_URL,
            'DEFAULT_TIMEOUT': 500,
            'SSL_CERT_REQS': None
        }
    }
