from .environment import env


class Redis(object):
    REDIS_URL = env('REDIS_URL')

    @property
    def CACHES(self):
        cache_config = {
            'default': env.cache_url(var='REDIS_URL')
        }

        cache_config['default']['OPTIONS'] = {
            'SOCKET_TIMEOUT': 120,
            'SOCKET_CONNECT_TIMEOUT': 30,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True
        }

        return cache_config

    @property
    def RQ_QUEUES(self):
        QUEUE_CONFIG = {
            'default': env.cache_url(var='REDIS_URL'),
            # Must be a separate queue as it's limited to one item at a time
            'wagtail_localize_pontoon.sync': env.cache_url(var='REDIS_URL'),
        }

        QUEUE_CONFIG['default']['DEFAULT_TIMEOUT'] = 500
        QUEUE_CONFIG['wagtail_localize_pontoon.sync']['DEFAULT_TIMEOUT'] = 500

        return QUEUE_CONFIG
