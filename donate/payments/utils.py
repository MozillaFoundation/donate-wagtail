from functools import lru_cache
from decimal import Decimal

from django.conf import settings

from .constants import (
    CURRENCIES,
    LOCALE_CURRENCY_MAP,
    PAYPAL_ACCOUNT_MACRO,
    PAYPAL_ACCOUNT_MICRO,
    ZERO_DECIMAL_CURRENCIES,
)


def zero_decimal_currency_fix(amount, currency):
    if currency.upper() not in ZERO_DECIMAL_CURRENCIES:
        return amount / 100

    return amount


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


def paypal_micro_fee(currency, amount):
    MICRO_FEE_PERCENT = Decimal('0.06')
    fee = amount * MICRO_FEE_PERCENT + Decimal(CURRENCIES[currency]['paypalFixedFee']['micro'])
    return fee.quantize(Decimal('0.01'))


def paypal_macro_fee(currency, amount):
    MACRO_FEE_PERCENT = Decimal('0.029')
    fee = amount * MACRO_FEE_PERCENT + Decimal(CURRENCIES[currency]['paypalFixedFee']['macro'])
    return fee.quantize(Decimal('0.01'))


def determine_paypal_account(currency, amount):
    """ Determine which paypal account to use for this currency."""
    micro_fee = paypal_micro_fee(currency, amount)
    macro_fee = paypal_macro_fee(currency, amount)
    return PAYPAL_ACCOUNT_MICRO if micro_fee <= macro_fee else PAYPAL_ACCOUNT_MACRO


def get_merchant_account_id_for_paypal(currency, amount):
    macro_merchant_account_id = settings.BRAINTREE_MERCHANT_ACCOUNTS[currency]
    # If the amount qualifies as a "micro" transaction, attempt to use the
    # merchant account specified for micro transactions, but fall back to the
    # macro one if not set.
    if determine_paypal_account(currency, amount) == PAYPAL_ACCOUNT_MICRO:
        return settings.BRAINTREE_MERCHANT_ACCOUNTS_PAYPAL_MICRO.get(
            currency, macro_merchant_account_id
        )
    return macro_merchant_account_id


@lru_cache(maxsize=1000)
def get_merchant_account_id_for_card(currency):
    return settings.BRAINTREE_MERCHANT_ACCOUNTS[currency]


@lru_cache(maxsize=1000)
def get_plan_id(currency):
    return settings.BRAINTREE_PLANS[currency]
