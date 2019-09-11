import os

import redis
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = os.getenv('REDIS_URL')

conn = redis.from_url(redis_url or 'redis://localhost:6379')

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "donate.settings")
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
