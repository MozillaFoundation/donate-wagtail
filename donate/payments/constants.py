from django.conf import settings


FREQUENCY_SINGLE = 'single'
FREQUENCY_MONTHLY = 'monthly'

FREQUENCIES = (FREQUENCY_SINGLE, FREQUENCY_MONTHLY)

FREQUENCY_CHOICES = (
    (FREQUENCY_SINGLE, 'Single'),
    (FREQUENCY_MONTHLY, 'Monthly'),
)

METHOD_CARD = 'Braintree_Card'
METHOD_PAYPAL = 'Braintree_Paypal'

PAYPAL_ACCOUNT_MICRO = 'micro'
PAYPAL_ACCOUNT_MACRO = 'macro'

METHODS = (METHOD_CARD, METHOD_PAYPAL)


CURRENCIES = settings.CURRENCIES

CURRENCY_CHOICES = tuple([
    (key, '{}   {}'.format(key.upper(), data['symbol'])) for key, data in CURRENCIES.items()
])


LOCALE_CURRENCY_MAP = {
    'ast': 'eur',
    'ca': 'eur',
    'cs': 'czk',
    'cy': 'gbp',
    'da': 'dkk',
    'de': 'eur',
    'dsb': 'eur',
    'el': 'eur',
    'en-AU': 'aud',
    'en-CA': 'cad',
    'en-GB': 'gbp',
    'en-IN': 'inr',
    'en-NZ': 'nzd',
    'en-US': 'usd',
    'es': 'eur',
    'es-MX': 'mxn',
    'es-XL': 'mxn',
    'et': 'eur',
    'fi': 'eur',
    'fr': 'eur',
    'fy-NL': 'eur',
    'gu-IN': 'inr',
    'hi-IN': 'inr',
    'hr': 'eur',
    'hsb': 'eur',
    'hu': 'huf',
    'it': 'eur',
    'ja': 'jpy',
    'kab': 'eur',
    'lv': 'eur',
    'ml': 'inr',
    'mr': 'inr',
    'nb-NO': 'nok',
    'nl': 'eur',
    'nn-NO': 'nok',
    'pa-IN': 'inr',
    'pl': 'pln',
    'pt-BR': 'brl',
    'pt-PT': 'eur',
    'ru': 'rub',
    'sk': 'eur',
    'sl': 'eur',
    'sv-SE': 'sek',
    'ta': 'inr',
    'te': 'inr',
    'zh-TW': 'twd'
}

ZERO_DECIMAL_CURRENCIES = [
  'BIF',
  'CLP',
  'DJF',
  'GNF',
  'JPY',
  'KMF',
  'KRW',
  'MGA',
  'PYG',
  'RWF',
  'VND',
  'VUV',
  'XAF',
  'XOF',
  'XPF'
]
