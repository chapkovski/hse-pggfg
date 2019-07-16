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
    num_rounds = 10
    rounds = list(range(1, num_rounds + 1))
    instructions_template = 'pggfg/Instructions.html'
    endowment = 20
    lb = c(10)
    ub = c(30)
    efficiency_factor = 2
    punishment_endowment = 10
    punishment_factor = 3
    configurable_params = ['gender_shown', 'hetero_endowment', 'punishment', 'timeout_contribution_points',
                           'timeout_contribution_seconds', 'random_contribution']


class Subsession(BaseSubsession):
    gender_shown = models.BooleanField(doc='whether the gender of other members of the groups will be shown')
    hetero_endowment = models.BooleanField(doc='whether the endowment is fixed or random')
    punishment = models.BooleanField(doc='whether game has a punihsment stage')
    timeout_contribution_points = models.CurrencyField(doc='In case of a fixed contribution how much?')
    timeout_contribution_seconds = models.IntegerField(doc='How many seconds a player has for decision on contribution')
    random_contribution = models.BooleanField(doc='will be contribution set randomly in case of timeout?')

    def get_average(self):
        all_contribs = [p.contribution or 0 for p in self.get_players()]
        return sum(all_contribs) / len(all_contribs)

    def vars_for_admin_report(self):
        session_contribs = [s.get_average() for s in self.in_rounds(1, Constants.num_rounds)]
        return {'series': session_contribs,
                'rounds': Constants.rounds}

    def set_config(self):
        for k in Constants.configurable_params:
            v = self.session.config.get(k)
            setattr(self, k, v)

    def creating_session(self):
        self.set_config()
        for p in self.get_players():
            if self.hetero_endowment:
                p.endowment = random.randint(Constants.lb, Constants.ub)
            else:
                p.endowment = Constants.endowment


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


class Player(BasePlayer):
    endowment = models.CurrencyField()
    contribution = models.PositiveIntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
        label="How much will you contribute to the project (from 0 to {})?".format(Constants.endowment)
    )
    punishment_sent = models.IntegerField()
    punishment_received = models.IntegerField()
    pd_payoff = models.CurrencyField(doc='to store payoff from contribution stage')
    punishment_endowment = models.IntegerField(initial=0, doc='punishment endowment')
    pun1, pun2, pun3 = [models.CurrencyField() for i in range(3)]

    def set_payoff(self):
        self.payoff = self.pd_payoff
        if self.subsession.punishment:
            self.payoff -= (self.punishment_sent + self.punishment_received)

    def set_punishment_endowment(self):
        assert self.pd_payoff is not None, 'You have to set pd_payoff before setting punishment endowment'
        self.punishment_endowment = min(self.pd_payoff, Constants.punishment_endowment)

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
