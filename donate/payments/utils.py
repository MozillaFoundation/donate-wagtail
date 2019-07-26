from functools import lru_cache

from .constants import CURRENCIES


def freeze_transaction_details_for_session(details):
    details = details.copy()
    details['amount'] = str(details['amount'])
    return details


@lru_cache(maxsize=1000)
def get_currency_info(currency):
    return CURRENCIES[currency].copy()
