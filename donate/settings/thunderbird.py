from .environment import app, env


class ThunderbirdOverrides(object):
    INSTALLED_APPS = ['donate.thunderbird']
    TEMPLATES_DIR = [app('thunderbird/templates')]
    FRONTEND = {
        'RELEASE_VERSION': env('HEROKU_RELEASE_VERSION'),
        'SENTRY_DSN': env('SENTRY_DSN'),
        'SENTRY_ENVIRONMENT': env('SENTRY_ENVIRONMENT'),
        'BRAINTREE_MERCHANT_ACCOUNTS': env('BRAINTREE_MERCHANT_ACCOUNTS'),
        'PAYPAL_DISPLAY_NAME': 'MZLA Technologies'
    }
    CURRENCIES = {
        'usd': {
            'code': 'usd',
            'minAmount': {
                'single': 2,
                'monthly': 2,
            },
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
            'minAmount': {
                'single': 3,
                'monthly': 3,
            },
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
            'minAmount': {
                'single': 8,
                'monthly': 8,
            },
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
            'minAmount': {
                'single': 3,
                'monthly': 3,
            },
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
            'minAmount': {
                'single': 2,
                'monthly': 2,
            },
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
            'minAmount': {
                'single': 45,
                'monthly': 45,
            },
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
            'minAmount': {
                'single': 13,
                'monthly': 13,
            },
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
            'minAmount': {
                'single': 2,
                'monthly': 2,
            },
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
            'minAmount': {
                'single': 2,
                'monthly': 2,
            },
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
            'minAmount': {
                'single': 15,
                'monthly': 15,
            },
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
            'minAmount': {
                'single': 570,
                'monthly': 570,
            },
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
            'minAmount': {
                'single': 145,
                'monthly': 145,
            },
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
            'minAmount': {
                'single': 230,
                'monthly': 230,
            },
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
            'minAmount': {
                'single': 40,
                'monthly': 40,
            },
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
            'minAmount': {
                'single': 17,
                'monthly': 17,
            },
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
            'minAmount': {
                'single': 3,
                'monthly': 3,
            },
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
            'minAmount': {
                'single': 7,
                'monthly': 7,
            },
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
            'minAmount': {
                'single': 130,
                'monthly': 130,
            },
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
            'minAmount': {
                'single': 18,
                'monthly': 18,
            },
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
            'minAmount': {
                'single': 62,
                'monthly': 62,
            },
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
