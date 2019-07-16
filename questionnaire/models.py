from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1
    GENDER_CHOICES = [(0, 'Male'), (1, 'Female'), (2, 'Other')]
    income_categories = ['<500', '500-1000', '1000-2000', '2000-4000', '4000-6000', 'More than 6000']
    INCOME_CHOICES = [(i, j) for i, j in enumerate(income_categories)]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(min=18, max=90, label='How old are you?')
    gender = models.IntegerField(choices=Constants.GENDER_CHOICES, widget=widgets.RadioSelectHorizontal,
                                 label='What is your gender?')
    income = models.IntegerField(choices=Constants.INCOME_CHOICES, widget=widgets.RadioSelect,
                                 label='What is your monthly income?')
