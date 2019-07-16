from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, Player
import random


class StartWP(WaitPage):
    pass


class Intro(Page):
    template_name = 'pggfg/Introduction.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

class IntroPunishment(Page):
    def is_displayed(self) -> bool:
        return self.round_number == self.session.config['punishment_round']

class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


    def vars_for_template(self):
        label = f'Сколько вы вкладываете в общий счет (от 0 до {self.player.endowment})?'
        return {'label': label, }

    def contribution_max(self):
        return self.player.endowment


class AfterContribWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_pd_payoffs()
        for p in self.group.get_players():
            p.set_punishment_endowment()


class Punishment(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.subsession.punishment

    def get_form_fields(self):
        return ['pun{}'.format(p.id_in_group) for p in self.player.get_others_in_group()]

    def vars_for_template(self):
        others = self.player.get_others_in_group()
        form = self.get_form()
        data = zip(others, form)
        return {'data': data}

    def error_message(self, values):
        tot_pun = sum([int(i) for i in values.values()])
        if tot_pun > self.player.punishment_endowment:
            return 'You can\'t send more than {} in total'.format(self.player.punishment_endowment)


class AfterPunishmentWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_final_payoffs()


class Results(Page):
    pass


page_sequence = [
    StartWP,
    Intro,
    IntroPunishment,
    Contribute,
    AfterContribWP,
    Punishment,
    AfterPunishmentWP,
    Results,
]
