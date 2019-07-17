from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, Player
import random
from django.core import validators


class Welcome(Page):
    form_fields = ['user_id']
    form_model = 'player'

    def is_displayed(self) -> bool:
        return self.round_number == 1

    def before_next_page(self):
        self.participant.label = str(self.player.user_id)


class StartWP(WaitPage):
    pass


class Intro(Page):
    template_name = 'pggfg/Introduction.html'

    def is_displayed(self):
        return self.subsession.round_number == 1


class CompMixin:
    def get_form(self, *args, **kwargs):
        f = super().get_form(*args, **kwargs)
        for i, j in f.fields.items():
            regex = rf'^{str(Constants.correct_answers.get(i))}$'
            j.validators.append(validators.RegexValidator(message='Проверьте правильность ответа', regex=regex,
                                                          code='invalid_input'))
        return f


class CQ1(CompMixin, Page):
    form_model = 'player'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def get_form_fields(self):
        fields = [f.name for f in Player._meta.get_fields() if f.name.startswith('cq')]

        return fields


class IntroPunishment(Page):
    def is_displayed(self) -> bool:
        return self.round_number == self.session.config['punishment_round']


class CQ2(CompMixin, Page):
    form_model = 'player'

    def is_displayed(self) -> bool:
        return self.round_number == self.session.config['punishment_round']

    def get_form_fields(self):
        fields = [f.name for f in Player._meta.get_fields() if f.name.startswith('pcq')]
        return fields


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
            return f'Вы не можете послать вычетов больше чем {self.player.punishment_endowment}'


class AfterPunishmentWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_final_payoffs()


class Results(Page):
    pass


class FinalResults(Page):
    def is_displayed(self) -> bool:
        return self.round_number == Constants.num_rounds

    def vars_for_template(self) -> dict:
        return {'real_payoff': self.participant.payoff.to_real_world_currency(self.session)}


page_sequence = [
    Welcome,
    Gender,
    StartWP,
    Intro,
    CQ1,
    IntroPunishment,
    CQ2,
    Contribute,
    AfterContribWP,
    Punishment,
    AfterPunishmentWP,
    Results,
    FinalResults,
]
