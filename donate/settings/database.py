from .environment import env


class Database(object):

    @property
    def DATABASES(self):
        config = {
            'default': env.db_url_config(env('DATABASE_URL'))
        }
        config['default']['ATOMIC_REQUESTS'] = True

        return config
