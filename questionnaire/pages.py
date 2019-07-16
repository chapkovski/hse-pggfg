from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Q(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'income']

    def before_next_page(self):
        self.participant.vars['gender'] = self.player.get_gender_display()


page_sequence = [
    Q,
]
