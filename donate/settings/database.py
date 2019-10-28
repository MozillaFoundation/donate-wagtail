from .environment import env


class Database(object):
    @classmethod
    def pre_setup(cls):
        cls.DATABASES['default'] = env.db_url(var='DATABASE_URL')
        cls.DATABASES['default']['ATOMIC_REQUESTS'] = True
