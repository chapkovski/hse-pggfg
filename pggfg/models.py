from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = "Philip Chapkovski, chapkovski@gmail.com"

doc = """
Public Good Game with Punishment (Fehr and Gaechter).
Fehr, E. and Gachter, S., 2000.
 Cooperation and punishment in public goods experiments. American Economic Review, 90(4), pp.980-994.
"""


class Constants(BaseConstants):
    name_in_url = 'pggfg'
    players_per_group = 3
    num_others_per_group = players_per_group - 1
    num_rounds = 20
    rounds = list(range(1, num_rounds + 1))
    instructions_template = 'pggfg/includes/Instructions.html'
    endowment = 20
    efficiency_factor = 1.5
    coef_factor = round(efficiency_factor / players_per_group, 2)
    punishment_endowment = 6
    punishment_factor = 3
    correct_answers = {'cq1_a': 20,
                       'cq1_b': 20,
                       'cq2_a': 30,
                       'cq2_b': 30,
                       'cq3_a': 32,
                       'cq3_b': 25,
                       'cq3_c': 18,
                       'cq4_a': 20,
                       'cq4_b': 20,
                       'cq4_c': 40,
                       'pcq1': 0,
                       'pcq2': 0,
                       'pcq3': 12,
                       'pcq4': 30,
                       }


class Subsession(BaseSubsession):
    punishment = models.BooleanField(doc='whether game has a punihsment stage')
    gender = models.BooleanField(doc='whether game has a punishment stage')

    def get_average(self):
        all_contribs = [p.contribution or 0 for p in self.get_players()]
        return sum(all_contribs) / len(all_contribs)

    def vars_for_admin_report(self):
        session_contribs = [s.get_average() for s in self.in_rounds(1, Constants.num_rounds)]
        return {'series': session_contribs,
                'rounds': Constants.rounds}

    def creating_session(self):
        if self.round_number < self.session.config['punishment_round']:
            self.punishment = False
        else:
            self.punishment = True

        self.gender = self.session.config.get('gender')

        for p in self.get_players():
            p.endowment = Constants.endowment
            p.set_punishment_endowment()


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    average_contribution = models.FloatField()
    individual_share = models.CurrencyField()

    def set_pd_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.average_contribution = self.total_contribution / Constants.players_per_group
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.set_pd_payoff()

    def set_final_payoffs(self):
        for p in self.get_players():
            p.set_punishment()
            p.set_payoff()


YOUR_PROFIT_LABEL = "Каким будет Ваш общий выигрыш в текущем периоде?"
AVERAGE_OTHER_PROF_LABEL = "Каким будет средний выигрыш двух других участников из вашей группы в текущем периоде (ECU)?"
SECOND_PROF_LABEL = "Каким будет общий выигрыш второго участника из вашей группы в текущем периоде (ECU)?"
THIRD_PROF_LABEL = "Каким будет общий выигрыш третьего участника из вашей группы в текущем периоде (ECU)?"


class Player(BasePlayer):
    ########### BLOCK: CQ - Part 1 ##############################################################
    cq1_a = models.CurrencyField(label=YOUR_PROFIT_LABEL)
    cq1_b = models.CurrencyField(
        label=AVERAGE_OTHER_PROF_LABEL)

    cq2_a = models.CurrencyField(label=YOUR_PROFIT_LABEL)
    cq2_b = models.CurrencyField(
        label=AVERAGE_OTHER_PROF_LABEL)

    cq3_a = models.CurrencyField(label=YOUR_PROFIT_LABEL)
    cq3_b = models.CurrencyField(
        label=SECOND_PROF_LABEL)
    cq3_c = models.CurrencyField(
        label=THIRD_PROF_LABEL)

    cq4_a = models.CurrencyField(label=YOUR_PROFIT_LABEL)
    cq4_b = models.CurrencyField(
        label=SECOND_PROF_LABEL)
    cq4_c = models.CurrencyField(
        label=THIRD_PROF_LABEL)

    ############ END OF: CQ #############################################################
    ########### BLOCK: CQ for Punishment stage ##############################################################
    pcq1 = models.CurrencyField()
    pcq2 = models.CurrencyField()
    pcq3 = models.CurrencyField()
    pcq4 = models.CurrencyField()
    ############ END OF: CQ for Punishment stage #############################################################
    user_id = models.IntegerField(label='Введите номер указанный на табличке у вас на столе')
    gender = models.IntegerField(label='', choices=((0, 'Мужчина'), (1, 'Женщина'), (2, 'Другой выбор')),
                                 widget=widgets.RadioSelect)
    endowment = models.CurrencyField()
    contribution = models.PositiveIntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
        label=f"How much will you contribute to the project (from 0 to {Constants.endowment})?"
    )
    punishment_sent = models.IntegerField()
    punishment_received = models.IntegerField()
    pd_payoff = models.CurrencyField(doc='to store payoff from contribution stage')
    punishment_endowment = models.CurrencyField(initial=0, doc='punishment endowment')
    pun1, pun2, pun3 = [models.CurrencyField(min=0, max=Constants.punishment_endowment) for i in range(3)]

    def user_id_error_message(self, value):
        ids = self.subsession.player_set.filter(user_id__isnull=False).values_list("user_id", flat=True)
        if value in ids:
            return 'Такой номер уже есть, попробуйте еще раз.'

    def set_payoff(self):
        self.payoff = self.pd_payoff
        if self.subsession.punishment:
            self.payoff -= (self.punishment_sent + self.punishment_received)

    def set_punishment_endowment(self):
        # TODO: it is not the proper way of doing this but a temporary fix
        # TODO: because theoretically they can have more for punishment than their own income (unlikely)
        self.punishment_endowment = Constants.punishment_endowment

    def set_punishment(self):
        puns_sent = [getattr(self, 'pun{}'.format(p.id_in_group)) for p in self.get_others_in_group()]
        puns_received = [getattr(p, 'pun{}'.format(self.id_in_group)) for p in self.get_others_in_group()]
        if self.subsession.punishment:
            self.punishment_sent = int(sum(puns_sent))
            self.punishment_received = int(sum(puns_received)) * Constants.punishment_factor
        else:
            self.punishment_sent = 0
            self.punishment_received = 0

    def set_pd_payoff(self):
        self.pd_payoff = sum([+ self.endowment,
                              - self.contribution,
                              + self.group.individual_share,
                              ])

    def charts(self):
        group_average = [round(p.group.average_contribution) if p.group.average_contribution else '' for p
                         in self.in_rounds(1, Constants.num_rounds)]
        my_contribs = [p.contribution if p.contribution else '' for p in self.in_rounds(1, Constants.num_rounds)]

        return {'rounds': Constants.rounds,
                'group_average': group_average,
                'individual_contributions': my_contribs}
