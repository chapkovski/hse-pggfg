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
        'name': 'questionnaire',
        'display_name': "Questionnaire",
        'num_demo_participants': 1,
        'app_sequence': ['questionnaire'],
    },
    {
        'name': 'my_first_app',
        'display_name': "My First App",
        'num_demo_participants': 1,
        'app_sequence': ['first_app'],
    },
    {
        'name': 'bmi_mono',
        'display_name': "BMI - single",
        'num_demo_participants': 2,
        'app_sequence': ['bmi'],
        'duo': False
    },
    {
        'name': 'bmi_duo',
        'display_name': "BMI - duo",
        'num_demo_participants': 2,
        'app_sequence': ['bmi'],
        'duo': True
    },
    {
        'name': 'pgg_baseline',
        'display_name': "Public Good Game - baseline",
        'num_demo_participants': 3,
        'app_sequence': ['pggfg'],
    },
    {
        'name': 'pgg_hetero',
        'display_name': "Public Good Game - Hetero endowment",
        'num_demo_participants': 3,
        'app_sequence': ['pggfg'],
        'hetero_endowment': True,
        'gender_shown': False,
        'punishment': False
    },
    {
        'name': 'pgg_gender',
        'display_name': "Public Good Game - Gender",
        'num_demo_participants': 3,
        'app_sequence': ['questionnaire', 'pggfg'],
        'hetero_endowment': False,
        'gender_shown': True,
        'punishment': False
    },
    {
        'name': 'pgg_punishment',
        'display_name': "Public Good Game - Punishment",
        'num_demo_participants': 3,
        'app_sequence': ['pggfg'],
        'hetero_endowment': False,
        'gender_shown': False,
        'punishment': True
    },
    {
        'name': 'pgg_timeout',
        'display_name': "Public Good Game with timeouts",
        'num_demo_participants': 3,
        'app_sequence': ['pggfg'],
        'hetero_endowment': False,
        'gender_shown': False,
        'punishment': False,
        'timeout_contribution_points': 0,
        'timeout_contribution_seconds': 20,
        'random_contribution': False,
    },
    {
        'name': 'trust',
        'display_name': "Trust",
        'num_demo_participants': 2,
        'app_sequence': ['questionnaire', 'trust'],
        'mono': True
    },
]
for i in SESSION_CONFIGS:
    i.setdefault('use_browser_bots', False)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [{'name': 'goettingen', 'display_name': 'Room for Goettingen Workshop'}]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '+qbflu%yq+u0$br#xte7$klu*k55byl*yw7_$mhk^a!msth_1t'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
