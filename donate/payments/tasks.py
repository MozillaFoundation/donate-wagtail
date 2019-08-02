from rq import Queue
from worker import conn


queue = Queue(connection=conn)


def send_newsletter_subscription_to_basket(data):
    pass


def send_transaction_to_basket(data):
    pass
