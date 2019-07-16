from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [

    {
        'name': 'pgg_punishment',
        'display_name': "Public Good Game - Punishment",
        'num_demo_participants': 3,
        'app_sequence': ['pggfg'],
        'punishment_round': 6
    },

]
USE_L10N = False
DECIMAL_SEPARATOR = '.'
for i in SESSION_CONFIGS:
    i.setdefault('use_browser_bots', False)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ru'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'ECU'
ROOMS = [{'name': 'hse',
          'display_name': 'Summer School (HSE)'}]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '+qbflu%yq+u0$br#xte7$klu*k55byl*yw7_$mhk^a!msth_1t'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'pggfg']
