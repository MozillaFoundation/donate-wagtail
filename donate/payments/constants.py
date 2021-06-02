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


CURRENCIES = {
    'usd': {
        'code': 'usd',
        'minAmount': 2,
        'symbol': '$',
        'paypalFixedFee': {
            'macro': 0.30,
            'micro': 0.05
        },
        'monthlyUpgrade': [
            {'min': 300, 'value': 30},
            {'min': 200, 'value': 20},
            {'min': 100, 'value': 10},
            {'min': 70, 'value': 7},
            {'min': 35, 'value': 5},
            {'min': 15, 'value': 3},
        ],
        'presets': {
            'single': [10, 20, 30, 60],
            'monthly': [5, 10, 15, 20],
        }
    },
    'aud': {
        'code': 'aud',
        'minAmount': 3,
        'symbol': '$',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 0.30,
            'micro': 0.05
        },
        'monthlyUpgrade': [
            {'min': 432, 'value': 40},
            {'min': 288, 'value': 30},
            {'min': 144, 'value': 15},
            {'min': 99, 'value': 10},
            {'min': 50, 'value': 7},
            {'min': 22, 'value': 4},
        ],
        'presets': {
            'single': [10, 20, 30, 60],
            'monthly': [5, 10, 15, 20],
        }
    },
    'brl': {
        'code': 'brl',
        'minAmount': 8,
        'symbol': 'R$',
        'paypalFixedFee': {
            'macro': 0.60,
            'micro': 0.10
        },
        'disabled': ['amex'],
        'monthlyUpgrade': [
            {'min': 1137, 'value': 100},
            {'min': 758, 'value': 75},
            {'min': 379, 'value': 35},
            {'min': 265, 'value': 25},
            {'min': 133, 'value': 20},
            {'min': 57, 'value': 10},
        ],
        'presets': {
            'single': [80, 40, 20, 10],
            'monthly': [40, 20, 10, 8]
        }
    },
    'cad': {
        'code': 'cad',
        'minAmount': 3,
        'symbol': '$',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 0.30,
            'micro': 0.05
        },
        'monthlyUpgrade': [
            {'min': 393, 'value': 40},
            {'min': 262, 'value': 25},
            {'min': 131, 'value': 12},
            {'min': 92, 'value': 9},
            {'min': 46, 'value': 6},
            {'min': 20, 'value': 4},
        ],
        'presets': {
            'single': [10, 20, 30, 60],
            'monthly': [5, 10, 15, 20],
        }
    },
    'chf': {
        'code': 'chf',
        'minAmount': 2,
        'symbol': 'Fr.',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 0.55,
            'micro': 0.09
        },
        'monthlyUpgrade': [
            {'min': 297, 'value': 30},
            {'min': 198, 'value': 20},
            {'min': 99, 'value': 10},
            {'min': 69, 'value': 7},
            {'min': 35, 'value': 5},
            {'min': 15, 'value': 3},
        ],
        'presets': {
            'single': [10, 20, 30, 60],
            'monthly': [5, 10, 15, 20],
        }
    },
    'czk': {
        'code': 'czk',
        'minAmount': 45,
        'symbol': 'Kč',
        'paypalFixedFee': {
            'macro': 10.00,
            'micro': 1.67
        },
        'disabled': ['amex'],
        'monthlyUpgrade': [
            {'min': 6870, 'value': 700},
            {'min': 4580, 'value': 450},
            {'min': 2290, 'value': 225},
            {'min': 1603, 'value': 150},
            {'min': 802, 'value': 100},
            {'min': 344, 'value': 65},
        ],
        'presets': {
            'single': [450, 220, 110, 70],
            'monthly': [220, 110, 70, 45]
        }
    },
    'dkk': {
        'code': 'dkk',
        'minAmount': 13,
        'symbol': 'kr',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 2.60,
            'micro': 0.43
        },
        'monthlyUpgrade': [
            {'min': 2007, 'value': 200},
            {'min': 1338, 'value': 125},
            {'min': 669, 'value': 60},
            {'min': 468, 'value': 45},
            {'min': 234, 'value': 30},
            {'min': 100, 'value': 20},
        ],
        'presets': {
            'single': [130, 60, 30, 20],
            'monthly': [60, 30, 20, 15]
        }
    },
    'eur': {
        'code': 'eur',
        'minAmount': 2,
        'symbol': '€',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 0.35,
            'micro': 0.05
        },
        'monthlyUpgrade': [
            {'min': 270, 'value': 25},
            {'min': 180, 'value': 20},
            {'min': 90, 'value': 10},
            {'min': 63, 'value': 6},
            {'min': 32, 'value': 5},
        ],
        'presets': {
            'single': [10, 20, 30, 60],
            'monthly': [5, 10, 15, 20],
        }
    },
    'gbp': {
        'code': 'gbp',
        'minAmount': 2,
        'symbol': '£',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 0.20,
            'micro': 0.05
        },
        'monthlyUpgrade': [
            {'min': 240, 'value': 25},
            {'min': 160, 'value': 15},
            {'min': 80, 'value': 10},
            {'min': 56, 'value': 5},
            {'min': 28, 'value': 4},
            {'min': 12, 'value': 3},
        ],
        'presets': {
            'single': [10, 20, 30, 60],
            'monthly': [5, 10, 15, 20]
        }
    },
    'hkd': {
        'code': 'hkd',
        'minAmount': 15,
        'symbol': '$',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 2.35,
            'micro': 0.39
        },
        'monthlyUpgrade': [
            {'min': 2343, 'value': 200},
            {'min': 1562, 'value': 150},
            {'min': 781, 'value': 75},
            {'min': 547, 'value': 50},
            {'min': 273, 'value': 40},
            {'min': 117, 'value': 25},
        ],
        'presets': {
            'single': [100, 50, 25, 18],
            'monthly': [70, 30, 20, 15]
        }
    },
    'huf': {
        'code': 'huf',
        'minAmount': 570,
        'symbol': 'Ft',
        'paypalFixedFee': {
            'macro': 90,
            'micro': 15
        },
        'disabled': ['amex'],
        'monthlyUpgrade': [
            {'min': 87600, 'value': 8000},
            {'min': 58400, 'value': 5000},
            {'min': 29200, 'value': 3000},
            {'min': 20400, 'value': 2000},
            {'min': 10200, 'value': 1500},
            {'min': 4380, 'value': 900},
        ],
        'zeroDecimal': 'paypal',
        'presets': {
            'single': [5600, 2800, 1400, 850],
            'monthly': [2800, 1400, 850, 600]
        }
    },
    'inr': {
        'code': 'inr',
        'minAmount': 145,
        'symbol': '₹',
        'disabled': ['paypal', 'amex'],
        'monthlyUpgrade': [
            {'min': 20700, 'value': 2000},
            {'min': 13800, 'value': 1000},
            {'min': 6900, 'value': 700},
            {'min': 4830, 'value': 500},
            {'min': 2415, 'value': 350},
            {'min': 1035, 'value': 200},
        ],
        'presets': {
            'single': [1000, 500, 350, 200],
            'monthly': [650, 350, 200, 130]
        }
    },
    'jpy': {
        'code': 'jpy',
        'minAmount': 230,
        'symbol': '¥',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 40,
            'micro': 7
        },
        'zeroDecimal': 'paypal',
        'monthlyUpgrade': [
            {'min': 32580, 'value': 3000},
            {'min': 21720, 'value': 2000},
            {'min': 10860, 'value': 1000},
            {'min': 7602, 'value': 750},
            {'min': 3801, 'value': 500},
            {'min': 1629, 'value': 300},
        ],
        'presets': {
            'single': [2240, 1120, 560, 340],
            'monthly': [1120, 560, 340, 230]
        }
    },
    'mxn': {
        'code': 'mxn',
        'minAmount': 40,
        'symbol': '$',
        'paypalFixedFee': {
            'macro': 4.00,
            'micro': 0.55
        },
        'disabled': ['amex'],
        'monthlyUpgrade': [
            {'min': 5700, 'value': 500},
            {'min': 3800, 'value': 350},
            {'min': 1900, 'value': 200},
            {'min': 1330, 'value': 125},
            {'min': 665, 'value': 100},
            {'min': 285, 'value': 50},
        ],
        'presets': {
            'single': [400, 200, 100, 60],
            'monthly': [200, 100, 60, 40]
        }
    },
    'nok': {
        'code': 'nok',
        'minAmount': 17,
        'symbol': 'kr',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 2.80,
            'micro': 0.47
        },
        'monthlyUpgrade': [
            {'min': 2598, 'value': 250},
            {'min': 1732, 'value': 175},
            {'min': 866, 'value': 80},
            {'min': 606, 'value': 60},
            {'min': 303, 'value': 40},
            {'min': 130, 'value': 25},
        ],
        'presets': {
            'single': [160, 80, 40, 20],
            'monthly': [100, 60, 30, 20]
        }
    },
    'nzd': {
        'code': 'nzd',
        'minAmount': 3,
        'symbol': '$',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 0.45,
            'micro': 0.08
        },
        'monthlyUpgrade': [
            {'min': 450, 'value': 45},
            {'min': 300, 'value': 30},
            {'min': 150, 'value': 15},
            {'min': 105, 'value': 10},
            {'min': 52, 'value': 7},
            {'min': 23, 'value': 4},
        ],
        'presets': {
            'single': [10, 20, 30, 60],
            'monthly': [5, 10, 15, 20]
        }
    },
    'pln': {
        'code': 'pln',
        'minAmount': 7,
        'symbol': 'zł',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 1.35,
            'micro': 0.23
        },
        'monthlyUpgrade': [
            {'min': 1146, 'value': 100},
            {'min': 764, 'value': 75},
            {'min': 382, 'value': 35},
            {'min': 267, 'value': 25},
            {'min': 134, 'value': 20},
            {'min': 57, 'value': 10},
        ],
        'presets': {
            'single': [80, 40, 20, 10],
            'monthly': [40, 20, 10, 7]
        }
    },
    'rub': {
        'code': 'rub',
        'minAmount': 130,
        'symbol': '₽',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 10,
            'micro': 2
        },
        'monthlyUpgrade': [
            {'min': 18960, 'value': 2000},
            {'min': 12640, 'value': 1200},
            {'min': 6320, 'value': 600},
            {'min': 4424, 'value': 400},
            {'min': 2212, 'value': 300},
            {'min': 948, 'value': 200},
        ],
        'presets': {
            'single': [1300, 800, 500, 200],
            'monthly': [500, 300, 200, 130]
        }
    },
    'sek': {
        'code': 'sek',
        'minAmount': 18,
        'symbol': 'kr',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 3.25,
            'micro': 0.54
        },
        'monthlyUpgrade': [
            {'min': 2832, 'value': 250},
            {'min': 1888, 'value': 175},
            {'min': 944, 'value': 90},
            {'min': 661, 'value': 65},
            {'min': 330, 'value': 50},
            {'min': 142, 'value': 25},
        ],
        'presets': {
            'single': [180, 90, 45, 30],
            'monthly': [90, 45, 30, 18]
        }
    },
    'twd': {
        'code': 'twd',
        'minAmount': 62,
        'symbol': 'NT$',
        'disabled': ['amex'],
        'paypalFixedFee': {
            'macro': 10.00,
            'micro': 2.00
        },
        'zeroDecimal': 'paypal',
        'monthlyUpgrade': [
            {'min': 9300, 'value': 900},
            {'min': 6200, 'value': 600},
            {'min': 3100, 'value': 300},
            {'min': 2170, 'value': 200},
            {'min': 1085, 'value': 150},
            {'min': 465, 'value': 100},
        ],
        'presets': {
            'single': [480, 240, 150, 70],
            'monthly': [250, 150, 100, 62]
        }
    }
}

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


# List of countries and their respective post code formats if applicable.
# Used in post-code-validation.js to check whether or not we display a post code form item to the user.
# Source of data can be found here: https://gist.github.com/lkopocinski/bd4494588458f5a8cc8ffbd12a4deefd
# NOTE: This list is also found in donate/constants.py, any updates to this list should be made there/vice-versa.
COUNTRY_POST_CODES = [
    {
        'abbrev': 'AF',
        'name': 'Afghanistan',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'AX',
        'name': 'Aland Islands',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'AL',
        'name': 'Albania',
        'postal': '(120|122)[0-9]{2}',
    },
    {
        'abbrev': 'DZ',
        'name': 'Algeria',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'AS',
        'name': 'American Samoa',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'AD',
        'name': 'Andorra',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'AO',
        'name': 'Angola',
    },
    {
        'abbrev': 'AI',
        'name': 'Anguilla',
        'postal': 'AI-2640',
    },
    {
        'abbrev': 'AQ',
        'name': 'Antarctica',
    },
    {
        'abbrev': 'AG',
        'name': 'Antigua and Barbuda',
    },
    {
        'abbrev': 'AR',
        'name': 'Argentina',
        'postal': '[A-Z]{1}[0-9]{4}[A-Z]{3}',
    },
    {
        'abbrev': 'AM',
        'name': 'Armenia',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'AW',
        'name': 'Aruba',
    },
    {
        'abbrev': 'AU',
        'name': 'Australia',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'AT',
        'name': 'Austria',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'AZ',
        'name': 'Azerbaijan',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'BS',
        'name': 'Bahamas',
    },
    {
        'abbrev': 'BH',
        'name': 'Bahrain',
    },
    {
        'abbrev': 'BD',
        'name': 'Bangladesh',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'BB',
        'name': 'Barbados',
        'postal': 'BB[0-9]{5}',
    },
    {
        'abbrev': 'BY',
        'name': 'Belarus',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'BE',
        'name': 'Belgium',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'BZ',
        'name': 'Belize',
    },
    {
        'abbrev': 'BJ',
        'name': 'Benin',
    },
    {
        'abbrev': 'BM',
        'name': 'Bermuda',
        'postal': '[A-Z]{2}[0-9]{2}',
    },
    {
        'abbrev': 'BT',
        'name': 'Bhutan',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'BO',
        'name': 'Bolivia',
    },
    {
        'abbrev': 'BQ',
        'name': 'Bonaire',
    },
    {
        'abbrev': 'BA',
        'name': 'Bosnia and Herzegovina',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'BW',
        'name': 'Botswana',
    },
    {
        'abbrev': 'BV',
        'name': 'Bouvet Islands',
    },
    {
        'abbrev': 'BR',
        'name': 'Brazil',
        'postal': '[0-9]{5}-[0-9]{3}',
    },
    {
        'abbrev': 'IO',
        'name': 'British Indian Ocean Territory',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'BN',
        'name': 'Brunei',
        'postal': '[A-Z]{2}[0-9]{4}',
    },
    {
        'abbrev': 'BG',
        'name': 'Bulgaria',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'BF',
        'name': 'Burkina Faso',
    },
    {
        'abbrev': 'BI',
        'name': 'Burundi',
    },
    {
        'abbrev': 'KH',
        'name': 'Cambodia',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'CM',
        'name': 'Cameroon',
    },
    {
        'abbrev': 'CA',
        'name': 'Canada',
        'postal': '[A-Z][0-9][A-Z] ?[0-9][A-Z][0-9]',
    },
    {
        'abbrev': 'CI',
        'name': 'Canary Islands',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'CV',
        'name': 'Cape Verde',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'KY',
        'name': 'Cayman Islands',
        'postal': '[A-Z]{2}[0-9]-[0-9]{4}',
    },
    {
        'abbrev': 'CF',
        'name': 'Central African Republic',
    },
    {
        'abbrev': 'TD',
        'name': 'Chad',
    },
    {
        'abbrev': 'CI',
        'name': 'Channel Islands',
        'postal': '[A-Z]{2}[0-9]{2}',
    },
    {
        'abbrev': 'CL',
        'name': 'Chile',
        'postal': '[0-9]{7}',
    },
    {
        'abbrev': 'CN',
        'name': 'China, People\'s Republic',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'CX',
        'name': 'Christmas Island',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'CC',
        'name': 'Cocos (Keeling) Islands',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'CO',
        'name': 'Colombia',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'KM',
        'name': 'Comoros',
    },
    {
        'abbrev': 'CG',
        'name': 'Congo',
    },
    {
        'abbrev': 'CD',
        'name': 'Congo, The Democratic Republic of',
    },
    {
        'abbrev': 'CK',
        'name': 'Cook Islands',
    },
    {
        'abbrev': 'CR',
        'name': 'Costa Rica',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'CI',
        'name': 'Côte d\'Ivoire',
    },
    {
        'abbrev': 'HR',
        'name': 'Croatia',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'CU',
        'name': 'Cuba',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'CW',
        'name': 'Curacao',
    },
    {
        'abbrev': 'CY',
        'name': 'Cyprus',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'CZ',
        'name': 'Czech Republic',
        'postal': '[0-9]{3} [0-9]{2}',
    },
    {
        'abbrev': 'DK',
        'name': 'Denmark',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'DJ',
        'name': 'Djibouti',
    },
    {
        'abbrev': 'DM',
        'name': 'Dominica',
    },
    {
        'abbrev': 'DO',
        'name': 'Dominican Republic',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'TL',
        'name': 'East Timor',
    },
    {
        'abbrev': 'EC',
        'name': 'Ecuador',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'EG',
        'name': 'Egypt',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'SV',
        'name': 'El Salvador',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'GQ',
        'name': 'Equatorial Guinea',
    },
    {
        'abbrev': 'ER',
        'name': 'Eritrea',
    },
    {
        'abbrev': 'EE',
        'name': 'Estonia',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'SZ',
        'name': 'Eswatini',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'ET',
        'name': 'Ethiopia',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'FK',
        'name': 'Falkland Islands',
        'postal': 'FIQQ 1ZZ',
    },
    {
        'abbrev': 'FO',
        'name': 'Faroe Islands',
        'postal': '[0-9]{3}',
    },
    {
        'abbrev': 'FJ',
        'name': 'Fiji',
    },
    {
        'abbrev': 'FI',
        'name': 'Finland',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'FR',
        'name': 'France',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'GF',
        'name': 'French Guiana',
    },
    {
        'abbrev': 'PF',
        'name': 'French Polynesia',
        'postal': '987[0-9]{2}',
    },
    {
        'abbrev': 'TF',
        'name': 'French Southern Territories',
    },
    {
        'abbrev': 'GA',
        'name': 'Gabon',
    },
    {
        'abbrev': 'GM',
        'name': 'Gambia',
    },
    {
        'abbrev': 'GE',
        'name': 'Georgia',
    },
    {
        'abbrev': 'DE',
        'name': 'Germany',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'GH',
        'name': 'Ghana',
    },
    {
        'abbrev': 'GI',
        'name': 'Gibraltar',
        'postal': 'GX11 1AA',
    },
    {
        'abbrev': 'GR',
        'name': 'Greece',
        'postal': '[0-9]{3} [0-9]{2}',
    },
    {
        'abbrev': 'GL',
        'name': 'Greenland',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'GD',
        'name': 'Grenada',
    },
    {
        'abbrev': 'GP',
        'name': 'Guadeloupe',
        'postal': '971[0-9]{2}',
    },
    {
        'abbrev': 'GU',
        'name': 'Guam',
        'postal': '\\d{5}(?:[-\\s]\\d{4})?',
    },
    {
        'abbrev': 'GT',
        'name': 'Guatemala',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'GG',
        'name': 'Guernsey',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'GW',
        'name': 'Guinea-Bissau',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'GQ',
        'name': 'Guinea-Equatorial',
    },
    {
        'abbrev': 'GN',
        'name': 'Guinea Republic',
        'postal': '[0-9]{3}',
    },
    {
        'abbrev': 'GY',
        'name': 'Guyana (British)',
    },
    {
        'abbrev': 'GF',
        'name': 'Guyana (French)',
        'postal': '973[0-9]{2}',
    },
    {
        'abbrev': 'HT',
        'name': 'Haiti',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'HM',
        'name': 'Heard Island and McDonald Islands',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'HN',
        'name': 'Honduras',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'HK',
        'name': 'Hong Kong',
    },
    {
        'abbrev': 'HU',
        'name': 'Hungary',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'IS',
        'name': 'Iceland',
        'postal': '[0-9]{3}',
    },
    {
        'abbrev': 'IN',
        'name': 'India',
        'postal': '[1-9][0-9]{5}',
    },
    {
        'abbrev': 'ID',
        'name': 'Indonesia',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'IR',
        'name': 'Iran',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'IQ',
        'name': 'Iraq',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'IE',
        'name': 'Ireland, Republic of',
        'postal': '(?:^[AC-FHKNPRTV-Y][0-9]{2}|D6W)[ -]?[0-9AC-FHKNPRTV-Y]{4}$',
    },
    {
        'abbrev': 'IM',
        'name': 'Isle of Man',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'FK',
        'name': 'Islas Malvinas',
        'postal': 'FIQQ 1ZZ',
    },
    {
        'abbrev': 'IL',
        'name': 'Israel',
        'postal': '[0-9]{5}|[0-9]{7}',
    },
    {
        'abbrev': 'IT',
        'name': 'Italy',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'CI',
        'name': 'Ivory Coast',
    },
    {
        'abbrev': 'JM',
        'name': 'Jamaica',
    },
    {
        'abbrev': 'JP',
        'name': 'Japan',
        'postal': '[0-9]{3}-[0-9]{4}',
    },
    {
        'abbrev': 'JE',
        'name': 'Jersey',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'JO',
        'name': 'Jordan',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'KZ',
        'name': 'Kazakhstan',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'KE',
        'name': 'Kenya',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'KI',
        'name': 'Kiribati',
    },
    {
        'abbrev': 'KR',
        'name': 'Korea, Republic of',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'KP',
        'name': 'Korea, The D.P.R of',
    },
    {
        'abbrev': 'XK',
        'name': 'Kosovo',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'KW',
        'name': 'Kuwait',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'KG',
        'name': 'Kyrgyzstan',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'LA',
        'name': 'Laos',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'LV',
        'name': 'Latvia',
        'postal': 'LV-[0-9]{4}',
    },
    {
        'abbrev': 'LB',
        'name': 'Lebanon',
        'postal': '[0-9]{4} [0-9]{4}',
    },
    {
        'abbrev': 'LS',
        'name': 'Lesotho',
        'postal': '[0-9]{3}',
    },
    {
        'abbrev': 'LR',
        'name': 'Liberia',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'LY',
        'name': 'Libya',
    },
    {
        'abbrev': 'LI',
        'name': 'Liechtenstein',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'LT',
        'name': 'Lithuania',
        'postal': 'LT-[0-9]{5}',
    },
    {
        'abbrev': 'LU',
        'name': 'Luxembourg',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'MO',
        'name': 'Macau',
    },
    {
        'abbrev': 'MK',
        'name': 'Macedonia, Republic of',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'MG',
        'name': 'Madagascar',
        'postal': '[0-9]{3}',
    },
    {
        'abbrev': 'MW',
        'name': 'Malawi',
    },
    {
        'abbrev': 'MY',
        'name': 'Malaysia',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'MV',
        'name': 'Maldives',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'ML',
        'name': 'Mali',
    },
    {
        'abbrev': 'MT',
        'name': 'Malta',
        'postal': '[A-Z]{3} [0-9]{4}',
    },
    {
        'abbrev': 'MH',
        'name': 'Marshall Islands',
        'postal': '\\d{5}(?:[-\\s]\\d{4})?',
    },
    {
        'abbrev': 'MQ',
        'name': 'Martinique',
        'postal': '972[0-9]{2}',
    },
    {
        'abbrev': 'MR',
        'name': 'Mauritania',
    },
    {
        'abbrev': 'MU',
        'name': 'Mauritius',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'YT',
        'name': 'Mayotte',
        'postal': '976[0-9]{2}',
    },
    {
        'abbrev': 'MX',
        'name': 'Mexico',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'FM',
        'name': 'Micronesia (Federated States of)',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'MD',
        'name': 'Moldova, Republic of',
        'postal': 'MD-?[0-9]{4}',
    },
    {
        'abbrev': 'MC',
        'name': 'Monaco',
        'postal': '980[0-9]{2}',
    },
    {
        'abbrev': 'MN',
        'name': 'Mongolia',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'ME',
        'name': 'Montenegro',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'MS',
        'name': 'Montserrat',
        'postal': 'MSR [0-9]{4}',
    },
    {
        'abbrev': 'MA',
        'name': 'Morocco',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'MZ',
        'name': 'Mozambique',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'MM',
        'name': 'Myanmar',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'NA',
        'name': 'Namibia',
    },
    {
        'abbrev': 'NR',
        'name': 'Nauru',
    },
    {
        'abbrev': 'NP',
        'name': 'Nepal',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'NL',
        'name': 'Netherlands',
        'postal': '(?:NL-)?(\\d{4})\\s*([A-Z]{2})',
    },
    {
        'abbrev': 'NC',
        'name': 'New Caledonia',
        'postal': '988[0-9]{2}',
    },
    {
        'abbrev': 'NZ',
        'name': 'New Zealand',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'NI',
        'name': 'Nicaragua',
    },
    {
        'abbrev': 'NE',
        'name': 'Niger',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'NG',
        'name': 'Nigeria',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'NU',
        'name': 'Niue',
    },
    {
        'abbrev': 'MP',
        'name': 'Northern Mariana Islands',
        'postal': '^\\d{5}(?:[-\\s]\\d{4})?$',
    },
    {
        'abbrev': 'NO',
        'name': 'Norway',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'OM',
        'name': 'Oman',
        'postal': '[0-9]{3}',
    },
    {
        'abbrev': 'PK',
        'name': 'Pakistan',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'PW',
        'name': 'Palau',
        'postal': '\\d{5}(?:[-\\s]\\d{4})?',
    },
    {
        'abbrev': 'PS',
        'name': 'Palestine, State of',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'PA',
        'name': 'Panama',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'PG',
        'name': 'Papua New Guinea',
        'postal': '[0-9]{3}',
    },
    {
        'abbrev': 'PY',
        'name': 'Paraguay',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'PE',
        'name': 'Peru',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'PH',
        'name': 'Philippines',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'PN',
        'name': 'Pitcairn',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'PL',
        'name': 'Poland',
        'postal': '[0-9]{2}-[0-9]{3}',
    },
    {
        'abbrev': 'PT',
        'name': 'Portugal',
        'postal': '[0-9]{4}-[0-9]{3}',
    },
    {
        'abbrev': 'PR',
        'name': 'Puerto Rico',
        'postal': '\\d{5}(?:[-\\s]\\d{4})?',
    },
    {
        'abbrev': 'QA',
        'name': 'Qatar',
    },
    {
        'abbrev': 'RE',
        'name': 'Réunion',
        'postal': '974[0-9]{2}',
    },
    {
        'abbrev': 'RO',
        'name': 'Romania',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'RU',
        'name': 'Russian Federation',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'RW',
        'name': 'Rwanda',
    },
    {
        'abbrev': 'MP',
        'name': 'Saipan',
        'postal': '96950',
    },
    {
        'abbrev': 'WS',
        'name': 'Samoa',
        'postal': 'WS[0-9]{4}',
    },
    {
        'abbrev': 'SM',
        'name': 'San Marino',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'ST',
        'name': 'Sao Tome and Principe',
    },
    {
        'abbrev': 'SA',
        'name': 'Saudi Arabia',
        'postal': '[0-9]{5}(-[0-9]{4})?',
    },
    {
        'abbrev': 'SN',
        'name': 'Senegal',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'RS',
        'name': 'Serbia',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'SC',
        'name': 'Seychelles',
    },
    {
        'abbrev': 'SL',
        'name': 'Sierra Leone',
    },
    {
        'abbrev': 'SG',
        'name': 'Singapore',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'SK',
        'name': 'Slovakia',
        'postal': '[0-9]{3} [0-9]{2}',
    },
    {
        'abbrev': 'SI',
        'name': 'Slovenia',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'SB',
        'name': 'Solomon Islands',
    },
    {
        'abbrev': 'SO',
        'name': 'Somalia',
        'postal': '[A-Z]{2} [0-9]{5}',
    },
    {
        'abbrev': 'ZA',
        'name': 'South Africa',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'GS',
        'name': 'South Georgia and the South Sandwhich Islands',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'KR',
        'name': 'South Korea',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'SS',
        'name': 'South Sudan',
    },
    {
        'abbrev': 'ES',
        'name': 'Spain',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'LK',
        'name': 'Sri Lanka',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'BL',
        'name': 'St. Barthélemy',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'VI',
        'name': 'St. Croix',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'SE',
        'name': 'St. Eustatius',
    },
    {
        'abbrev': 'SH',
        'name': 'St. Helena',
        'postal': 'STHL 1ZZ',
    },
    {
        'abbrev': 'AG',
        'name': 'St. John',
        'postal': '\\d{5}(?:[-\\s]\\d{4})?',
    },
    {
        'abbrev': 'KN',
        'name': 'St. Kitts and Nevis',
        'postal': '[A-Z]{2}[0-9]{4}',
    },
    {
        'abbrev': 'LC',
        'name': 'St. Lucia',
        'postal': '[A-Z]{2}[0-9]{2} [0-9]{3}',
    },
    {
        'abbrev': 'SX',
        'name': 'St. Maarten',
    },
    {
        'abbrev': 'PM',
        'name': 'St.Pierre and Miquelon',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'VI',
        'name': 'St. Thomas',
    },
    {
        'abbrev': 'VC',
        'name': 'St. Vincent and the Grenadines',
        'postal': 'VC[0-9]{4}',
    },
    {
        'abbrev': 'SD',
        'name': 'Sudan',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'SR',
        'name': 'Suriname',
    },
    {
        'abbrev': 'SJ',
        'name': 'Svalbard and Jan Mayeb',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'SZ',
        'name': 'Swaziland',
        'postal': '[A-Z]{1}[0-9]{3}',
    },
    {
        'abbrev': 'SE',
        'name': 'Sweden',
        'postal': '[0-9]{3} [0-9]{2}',
    },
    {
        'abbrev': 'CH',
        'name': 'Switzerland',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'SY',
        'name': 'Syria',
    },
    {
        'abbrev': 'PF',
        'name': 'Tahiti',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'TW',
        'name': 'Taiwan',
        'postal': '[0-9]{3}(-[0-9]{2})?',
    },
    {
        'abbrev': 'TJ',
        'name': 'Tajikistan',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'TZ',
        'name': 'Tanzania',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'TH',
        'name': 'Thailand',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'TG',
        'name': 'Togo',
    },
    {
        'abbrev': 'TK',
        'name': 'Tokelau',
    },
    {
        'abbrev': 'TO',
        'name': 'Tonga',
    },
    {
        'abbrev': 'VG',
        'name': 'Tortola',
        'postal': 'VG[0-9]{4}',
    },
    {
        'abbrev': 'TT',
        'name': 'Trinidad and Tobago',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'TN',
        'name': 'Tunisia',
        'postal': '[0-9]{4}',
    },
    {
        'abbrev': 'TR',
        'name': 'Turkey',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'TM',
        'name': 'Turkmenistan',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'TC',
        'name': 'Turks and Caicos Islands',
        'postal': 'TKCA 1ZZ',
    },
    {
        'abbrev': 'TV',
        'name': 'Tuvalu',
    },
    {
        'abbrev': 'UG',
        'name': 'Uganda',
    },
    {
        'abbrev': 'UA',
        'name': 'Ukraine',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'AE',
        'name': 'United Arab Emirates',
    },
    {
        'abbrev': 'GB',
        'name': 'United Kingdom',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'UM',
        'name': 'United States Minor Outlying Islands',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'US',
        'name': 'United States of America',
        'postal': '\\d{5}(?:[-\\s]\\d{4})?',
    },
    {
        'abbrev': 'UY',
        'name': 'Uruguay',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'UZ',
        'name': 'Uzbekistan',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'VU',
        'name': 'Vanuatu',
    },
    {
        'abbrev': 'VE',
        'name': 'Venezuela',
        'postal': '[0-9]{4}(-[A-Z]{1})?',
    },
    {
        'abbrev': 'VN',
        'name': 'Vietnam',
        'postal': '[0-9]{6}',
    },
    {
        'abbrev': 'VG',
        'name': 'Virgin Islands (British)',
        'postal': 'VG[0-9]{4}',
    },
    {
        'abbrev': 'VI',
        'name': 'Virgin Islands (US)',
        'postal': '\\d{5}(?:[-\\s]\\d{4})?',
    },
    {
        'abbrev': 'WF',
        'name': 'Wallis and Futuna',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'EH',
        'name': 'Western Sahara',
    },
    {
        'abbrev': 'YE',
        'name': 'Yemen',
    },
    {
        'abbrev': 'ZM',
        'name': 'Zambia',
        'postal': '[0-9]{5}',
    },
    {
        'abbrev': 'ZW',
        'name': 'Zimbabwe',
    },
]
