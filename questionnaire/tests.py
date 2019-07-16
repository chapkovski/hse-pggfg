from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def play_round(self):
        yield pages.Q, {'gender': random.choice([0,1,2]),
                        'age': random.randint(18,90),
                        'income': random.choice(Constants.INCOME_CHOICES)[0]}