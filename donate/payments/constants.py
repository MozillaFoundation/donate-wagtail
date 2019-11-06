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
            'single': [50, 25, 10, 3],
            'monthly': [10, 5, 3, 2]
        }
    },
    'aed': {
        'code': 'aed',
        'minAmount': 8,
        'symbol': 'د.إ.‏',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 1100, 'value': 100},
            {'min': 734, 'value': 70},
            {'min': 367, 'value': 35},
            {'min': 257, 'value': 25},
            {'min': 128, 'value': 20},
            {'min': 55, 'value': 10},
        ],
        'presets': {
            'single': [55, 37, 18, 11],
            'monthly': [37, 18, 11, 8]
        }
    },
    'all': {
        'code': 'all',
        'minAmount': 230,
        'symbol': 'L',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 32000, 'value': 3000},
            {'min': 21800, 'value': 2000},
            {'min': 10900, 'value': 1000},
            {'min': 7360, 'value': 750},
            {'min': 3815, 'value': 500},
            {'min': 1635, 'value': 300},
        ],
        'presets': {
            'single': [2280, 1140, 570, 350],
            'monthly': [1140, 570, 350, 230]
        }
    },
    'aud': {
        'code': 'aud',
        'minAmount': 3,
        'symbol': '$',
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
            'single': [30, 15, 7, 4],
            'monthly': [15, 7, 4, 3]
        }
    },
    'ars': {
        'code': 'ars',
        'minAmount': 80,
        'symbol': '$',
        'disabled': ['paypal', 'amex'],
        'monthlyUpgrade': [
            {'min': 13000, 'value': 1300},
            {'min': 8780, 'value': 800},
            {'min': 4390, 'value': 400},
            {'min': 3073, 'value': 300},
            {'min': 1537, 'value': 200},
            {'min': 659, 'value': 125},
        ],
        'presets': {
            'single': [730, 370, 200, 110],
            'monthly': [370, 200, 110, 80]
        }
    },
    'azn': {
        'code': 'azn',
        'minAmount': 4,
        'symbol': '₼',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 500, 'value': 50},
            {'min': 340, 'value': 30},
            {'min': 170, 'value': 15},
            {'min': 119, 'value': 12},
            {'min': 60, 'value': 10},
            {'min': 26, 'value': 5},
        ],
        'presets': {
            'single': [34, 17, 8, 5],
            'monthly': [17, 8, 5, 4]
        }
    },
    'bam': {
        'code': 'bam',
        'minAmount': 4,
        'symbol': 'KM',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 500, 'value': 50},
            {'min': 350, 'value': 30},
            {'min': 175, 'value': 15},
            {'min': 123, 'value': 12},
            {'min': 61, 'value': 10},
            {'min': 26, 'value': 5},
        ],
        'presets': {
            'single': [32, 16, 8, 5],
            'monthly': [16, 8, 5, 4]
        }
    },
    'bdt': {
        'code': 'bdt',
        'minAmount': 170,
        'symbol': '৳',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 25000, 'value': 2500},
            {'min': 16892, 'value': 1600},
            {'min': 8446, 'value': 800},
            {'min': 5912, 'value': 600},
            {'min': 2956, 'value': 400},
            {'min': 1267, 'value': 250},
        ],
        'presets': {
            'single': [1700, 840, 420, 250],
            'monthly': [840, 420, 250, 170]
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
            'single': [65, 30, 15, 4],
            'monthly': [10, 7, 4, 3]
        }
    },
    'chf': {
        'code': 'chf',
        'minAmount': 2,
        'symbol': 'Fr.',
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
            'single': [20, 10, 5, 3],
            'monthly': [10, 5, 3, 2]
        }
    },
    'clp': {
        'code': 'clp',
        'minAmount': 1350,
        'symbol': '$',
        'disabled': ['paypal', 'amex'],
        'monthlyUpgrade': [
            {'min': 200000, 'value': 20000},
            {'min': 140160, 'value': 14000},
            {'min': 70080, 'value': 7000},
            {'min': 49056, 'value': 4500},
            {'min': 24528, 'value': 3500},
            {'min': 10512, 'value': 2000},
        ],
        'presets': {
            'single': [13000, 6500, 3250, 2000],
            'monthly': [6500, 3250, 2000, 1350]
        }
    },
    'cny': {
        'code': 'cny',
        'minAmount': 14,
        'symbol': '¥',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 2000, 'value': 200},
            {'min': 1376, 'value': 130},
            {'min': 688, 'value': 70},
            {'min': 482, 'value': 50},
            {'min': 241, 'value': 30},
            {'min': 103, 'value': 20},
        ],
        'presets': {
            'single': [140, 70, 35, 20],
            'monthly': [70, 35, 20, 14]
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
    'dzd': {
        'code': 'dzd',
        'minAmount': 240,
        'symbol': 'د.ج.‏',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 36000, 'value': 3600},
            {'min': 24000, 'value': 2400},
            {'min': 12000, 'value': 1200},
            {'min': 8400, 'value': 800},
            {'min': 4200, 'value': 600},
            {'min': 1800, 'value': 350},
        ],
        'presets': {
            'single': [2400, 1200, 600, 350],
            'monthly': [1200, 600, 350, 220]
        }
    },
    'egp': {
        'code': 'egp',
        'minAmount': 36,
        'symbol': 'ج.م.‏',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 5000, 'value': 500},
            {'min': 3310, 'value': 300},
            {'min': 1655, 'value': 150},
            {'min': 1159, 'value': 100},
            {'min': 579, 'value': 80},
            {'min': 248, 'value': 50},
        ],
        'presets': {
            'single': [360, 180, 90, 55],
            'monthly': [180, 90, 55, 36]
        }
    },
    'eur': {
        'code': 'eur',
        'minAmount': 2,
        'symbol': '€',
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
            'single': [50, 25, 10, 3],
            'monthly': [10, 5, 3, 2]
        }
    },
    'gbp': {
        'code': 'gbp',
        'minAmount': 2,
        'symbol': '£',
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
            'single': [20, 10, 5, 3],
            'monthly': [10, 5, 3, 2]
        }
    },
    'gel': {
        'code': 'gel',
        'minAmount': 5,
        'symbol': '₾',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 888, 'value': 90},
            {'min': 592, 'value': 60},
            {'min': 296, 'value': 30},
            {'min': 207, 'value': 20},
            {'min': 104, 'value': 15},
            {'min': 44, 'value': 10},
        ],
        'presets': {
            'single': [50, 25, 12, 7],
            'monthly': [25, 12, 7, 5]
        }
    },
    'gtq': {
        'code': 'gtq',
        'minAmount': 15,
        'symbol': 'Q',
        'disabled': ['paypal', 'amex'],
        'monthlyUpgrade': [
            {'min': 2310, 'value': 200},
            {'min': 1450, 'value': 150},
            {'min': 770, 'value': 70},
            {'min': 539, 'value': 50},
            {'min': 270, 'value': 40},
            {'min': 116, 'value': 20},
        ],
        'presets': {
            'single': [145, 70, 35, 20],
            'monthly': [70, 35, 20, 15]
        }
    },
    'hkd': {
        'code': 'hkd',
        'minAmount': 15,
        'symbol': '$',
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
    'hrk': {
        'code': 'hrk',
        'minAmount': 13,
        'symbol': 'kn',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 1992, 'value': 200},
            {'min': 1328, 'value': 130},
            {'min': 664, 'value': 60},
            {'min': 465, 'value': 45},
            {'min': 232, 'value': 30},
            {'min': 100, 'value': 20},
        ],
        'presets': {
            'single': [128, 64, 32, 19],
            'monthly': [64, 32, 19, 13]
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
    'idr': {
        'code': 'idr',
        'minAmount': 30000,
        'symbol': 'Rp',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 4208100, 'value': 400000},
            {'min': 2805400, 'value': 250000},
            {'min': 1402700, 'value': 140000},
            {'min': 981890, 'value': 100000},
            {'min': 490945, 'value': 70000},
            {'min': 210405, 'value': 40000},
        ],
        'presets': {
            'single': [300000, 150000, 75000, 45000],
            'monthly': [150000, 75000, 45000, 30000]
        }
    },
    'ils': {
        'code': 'ils',
        'minAmount': 8,
        'symbol': '₪',
        'paypalFixedFee': {
            'macro': 1.20,
            'micro': 0.20
        },
        'monthlyUpgrade': [
            {'min': 1056, 'value': 100},
            {'min': 704, 'value': 70},
            {'min': 352, 'value': 35},
            {'min': 246, 'value': 25},
            {'min': 123, 'value': 15},
            {'min': 53, 'value': 10},
        ],
        'presets': {
            'single': [60, 30, 15, 9],
            'monthly': [50, 20, 10, 8]
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
    'krw': {
        'code': 'krw',
        'minAmount': 2300,
        'symbol': '₩',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 354900, 'value': 35000},
            {'min': 236600, 'value': 23000},
            {'min': 118300, 'value': 10000},
            {'min': 82810, 'value': 8000},
            {'min': 41405, 'value': 6000},
            {'min': 17745, 'value': 3500},
        ],
        'presets': {
            'single': [22320, 11160, 5580, 3350],
            'monthly': [11160, 5580, 3350, 2300]
        }
    },
    'lak': {
        'code': 'lak',
        'minAmount': 17000,
        'symbol': '₭',
        'disabled': ['paypal', 'amex'],
        'monthlyUpgrade': [
            {'min': 2608500, 'value': 250000},
            {'min': 1739000, 'value': 170000},
            {'min': 869500, 'value': 85000},
            {'min': 608650, 'value': 60000},
            {'min': 304325, 'value': 40000},
            {'min': 130425, 'value': 25000},
        ],
        'presets': {
            'single': [160000, 80000, 40000, 25000],
            'monthly': [80000, 40000, 25000, 17000]
        }
    },
    'lbp': {
        'code': 'lbp',
        'minAmount': 3016,
        'symbol': 'ل.ل.‎',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 452100, 'value': 45000},
            {'min': 301400, 'value': 30000},
            {'min': 150700, 'value': 15000},
            {'min': 105490, 'value': 10000},
            {'min': 52745, 'value': 7500},
            {'min': 22605, 'value': 4000},
        ],
        'presets': {
            'single': [22623, 15082, 7541, 4525],
            'monthly': [15082, 7541, 4525, 3016]
        }
    },
    'mad': {
        'code': 'mad',
        'minAmount': 20,
        'symbol': 'MAD',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 2883, 'value': 300},
            {'min': 1922, 'value': 180},
            {'min': 961, 'value': 100},
            {'min': 673, 'value': 60},
            {'min': 336, 'value': 50},
            {'min': 144, 'value': 30},
        ],
        'presets': {
            'single': [150, 100, 50, 30],
            'monthly': [100, 50, 30, 20]
        }
    },
    'myr': {
        'code': 'myr',
        'minAmount': 9,
        'symbol': 'RM',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 1236, 'value': 120},
            {'min': 824, 'value': 80},
            {'min': 412, 'value': 40},
            {'min': 288, 'value': 25},
            {'min': 144, 'value': 20},
            {'min': 62, 'value': 12},
        ],
        'presets': {
            'single': [85, 42, 21, 13],
            'monthly': [42, 21, 13, 9]
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
            'single': [40, 20, 10, 4],
            'monthly': [20, 10, 8, 3]
        }
    },
    'php': {
        'code': 'php',
        'minAmount': 110,
        'symbol': '₱',
        'paypalFixedFee': {
            'macro': 15.00,
            'micro': 2.50
        },
        'monthlyUpgrade': [
            {'min': 15360, 'value': 1500},
            {'min': 10240, 'value': 1000},
            {'min': 5120, 'value': 500},
            {'min': 3584, 'value': 350},
            {'min': 1792, 'value': 250},
            {'min': 768, 'value': 150},
        ],
        'presets': {
            'single': [1000, 520, 260, 150],
            'monthly': [520, 260, 150, 90]
        }
    },
    'pln': {
        'code': 'pln',
        'minAmount': 7,
        'symbol': 'zł',
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
    'qar': {
        'code': 'qar',
        'minAmount': 8,
        'symbol': 'ر.ق.‏',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 1092, 'value': 100},
            {'min': 728, 'value': 70},
            {'min': 364, 'value': 35},
            {'min': 255, 'value': 25},
            {'min': 127, 'value': 20},
            {'min': 55, 'value': 10},
        ],
        'presets': {
            'single': [55, 36, 18, 11],
            'monthly': [36, 18, 11, 8]
        }
    },
    'ron': {
        'code': 'ron',
        'minAmount': 8,
        'symbol': 'lei',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 1275, 'value': 125},
            {'min': 850, 'value': 85},
            {'min': 425, 'value': 40},
            {'min': 298, 'value': 30},
            {'min': 149, 'value': 20},
            {'min': 64, 'value': 12},
        ],
        'presets': {
            'single': [80, 40, 20, 12],
            'monthly': [40, 20, 12, 8]
        }
    },
    'rub': {
        'code': 'rub',
        'minAmount': 130,
        'symbol': '₽',
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
    'sar': {
        'code': 'sar',
        'minAmount': 8,
        'symbol': 'ر.س.‏',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 1125, 'value': 100},
            {'min': 750, 'value': 75},
            {'min': 375, 'value': 40},
            {'min': 263, 'value': 25},
            {'min': 131, 'value': 20},
            {'min': 56, 'value': 10},
        ],
        'presets': {
            'single': [56, 37, 18, 11],
            'monthly': [37, 18, 11, 8]
        }
    },
    'sek': {
        'code': 'sek',
        'minAmount': 18,
        'symbol': 'kr',
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
    'sgd': {
        'code': 'sgd',
        'minAmount': 3,
        'symbol': '$SG',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 411, 'value': 40},
            {'min': 274, 'value': 25},
            {'min': 137, 'value': 15},
            {'min': 96, 'value': 10},
            {'min': 48, 'value': 7},
            {'min': 21, 'value': 4},
        ],
        'presets': {
            'single': [20, 14, 7, 4],
            'monthly': [14, 7, 4, 3]
        }
    },
    'thb': {
        'code': 'thb',
        'minAmount': 70,
        'symbol': '฿',
        'paypalFixedFee': {
            'macro': 11.00,
            'micro': 1.80
        },
        'monthlyUpgrade': [
            {'min': 9300, 'value': 900},
            {'min': 6200, 'value': 600},
            {'min': 3100, 'value': 300},
            {'min': 2170, 'value': 200},
            {'min': 1085, 'value': 150},
            {'min': 465, 'value': 100},
        ],
        'presets': {
            'single': [500, 250, 125, 75],
            'monthly': [300, 200, 100, 70]
        }
    },
    'try': {
        'code': 'try',
        'minAmount': 11,
        'symbol': '₺',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 1665, 'value': 150},
            {'min': 1110, 'value': 100},
            {'min': 555, 'value': 50},
            {'min': 389, 'value': 40},
            {'min': 194, 'value': 25},
            {'min': 83, 'value': 15},
        ],
        'presets': {
            'single': [100, 50, 25, 15],
            'monthly': [50, 25, 15, 11]
        }
    },
    'twd': {
        'code': 'twd',
        'minAmount': 62,
        'symbol': 'NT$',
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
    },
    'uah': {
        'code': 'uah',
        'minAmount': 60,
        'symbol': '₴',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 7530, 'value': 750},
            {'min': 5020, 'value': 500},
            {'min': 2510, 'value': 250},
            {'min': 1757, 'value': 170},
            {'min': 879, 'value': 100},
            {'min': 377, 'value': 75},
        ],
        'presets': {
            'single': [530, 260, 130, 80],
            'monthly': [260, 130, 80, 60]
        }
    },
    'yer': {
        'code': 'yer',
        'minAmount': 500,
        'symbol': 'ر.ي.‏',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 75000, 'value': 7500},
            {'min': 50000, 'value': 5000},
            {'min': 25000, 'value': 2500},
            {'min': 17500, 'value': 1750},
            {'min': 8750, 'value': 1250},
            {'min': 3750, 'value': 750},
        ],
        'presets': {
            'single': [3752, 2500, 1250, 750],
            'monthly': [2500, 1250, 750, 500]
        }
    },
    'zar': {
        'code': 'zar',
        'minAmount': 28,
        'symbol': 'R',
        'disabled': ['paypal'],
        'monthlyUpgrade': [
            {'min': 4260, 'value': 400},
            {'min': 2840, 'value': 275},
            {'min': 1420, 'value': 140},
            {'min': 994, 'value': 100},
            {'min': 497, 'value': 70},
            {'min': 213, 'value': 40},
        ],
        'presets': {
            'single': [275, 130, 70, 40],
            'monthly': [130, 70, 40, 28]
        }
    }
}

CURRENCY_CHOICES = tuple([
    (key, '{}   {}'.format(key.upper(), data['symbol'])) for key, data in CURRENCIES.items()
])


LOCALE_CURRENCY_MAP = {
    'ast': 'eur',
    'az': 'azn',
    'bn': 'bdt',
    'bs': 'bam',
    'ca': 'eur',
    'cak': 'gtq',
    'cs': 'czk',
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
    'en-ZA': 'zar',
    'es': 'eur',
    'es-AR': 'ars',
    'es-CL': 'clp',
    'es-EL': 'eur',
    'es-MX': 'mxn',
    'es-XL': 'mxn',
    'et': 'eur',
    'fi': 'eur',
    'fr': 'eur',
    'fy-NL': 'eur',
    'gu-IN': 'inr',
    'he': 'ils',
    'hi-IN': 'inr',
    'hr': 'hrk',
    'hsb': 'eur',
    'hu': 'huf',
    'id': 'idr',
    'it': 'eur',
    'ja': 'jpy',
    'ka': 'gel',
    'kab': 'dzd',
    'ko': 'krw',
    'lo': 'lak',
    'lv': 'eur',
    'ml': 'inr',
    'mr': 'inr',
    'ms': 'myr',
    'nb-NO': 'nok',
    'nl': 'eur',
    'nn-NO': 'nok',
    'pa-IN': 'inr',
    'pl': 'pln',
    'pt-BR': 'brl',
    'pt-PT': 'eur',
    'ro': 'ron',
    'ru': 'rub',
    'sk': 'eur',
    'sl': 'eur',
    'sq': 'all',
    'sv-SE': 'sek',
    'ta': 'inr',
    'te': 'inr',
    'th': 'thb',
    'tr': 'try',
    'uk': 'uah',
    'zh-CN': 'cny',
    'zh-TW': 'twd'
}
