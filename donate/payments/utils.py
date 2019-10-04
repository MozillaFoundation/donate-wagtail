from functools import lru_cache
from decimal import Decimal

from .constants import CURRENCIES, LOCALE_CURRENCY_MAP


def freeze_transaction_details_for_session(details):
    details = details.copy()
    details['amount'] = str(details['amount'])
    return details


@lru_cache(maxsize=1000)
def get_currency_info(currency):
    return CURRENCIES[currency].copy()


@lru_cache(maxsize=1000)
def get_default_currency(lang):
    """Return the best match for default currency for the user's locale."""
    try:
        return LOCALE_CURRENCY_MAP[lang]
    except KeyError:
        # Strip the region and attempt to find a currency that matches the base language
        code, _, country = lang.partition('-')
        try:
            return LOCALE_CURRENCY_MAP[code]
        except KeyError:
            pass

    return 'usd'


@lru_cache(maxsize=1000)
def get_suggested_monthly_upgrade(currency, single_amount):
    """
    Returns a suggested upgrade based on the single amount. If the amount is too
    low then this function will return None.
    """
    info = get_currency_info(currency)
    for tier in info.get('monthlyUpgrade', []):
        if Decimal(single_amount) >= tier['min']:
            return Decimal(tier['value'])
