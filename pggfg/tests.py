from otree.api import (
    Currency as c, currency_range, SubmissionMustFail, Submission
)
from .pages import *
from otree.api import Bot, SubmissionMustFail, Submission
from .models import Constants, Player
import random


class PlayerBot(Bot):

    def play_round(self):

        if self.round_number == 1:
            yield Welcome, {'user_id': self.player.id_in_subsession}
            if self.subsession.gender:
                yield Gender, {'gender': random.randint(0, 1)}
            yield Intro
            yield CQ1, {'cq1_a': 20,
                        'cq1_b': 20,
                        'cq2_a': 30,
                        'cq2_b': 30,
                        'cq3_a': 32,
                        'cq3_b': 25,
                        'cq3_c': 18,
                        'cq4_a': 20,
                        'cq4_b': 20,
                        'cq4_c': 40,
                        }
        if self.round_number == self.session.config['punishment_round']:
            yield IntroPunishment,
            yield CQ2, {
                'pcq1': 0,
                'pcq2': 0,
                'pcq3': 12,
                'pcq4': 30,
            }
        contribution = random.randint(0, self.player.endowment)

        yield Submission(Contribute, {'contribution': contribution}, timeout_happened=False)

        if self.subsession.punishment:
            pun_fields = ['pun{}'.format(p.id_in_group) for p in self.player.get_others_in_group()]
            _sum = self.player.punishment_endowment

            answers = dict(zip(pun_fields, [1 for _ in pun_fields]))
            yield Punishment, {**answers}
        yield Results
        if self.round_number == Constants.num_rounds:
            yield FinalResults,
