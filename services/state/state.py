#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for storing gameday state information."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/state', '', _path))

from common.datetime_.datetime_ import suffix  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.reference.reference import player_to_name_sub  # noqa
from common.teams.teams import encoding_to_abbreviation_sub  # noqa


class State(object):
    def __init__(self, data):
        self.away_team = data['away_team']
        self.home_team = data['home_team']

        self.runs = {self.away_team: 0, self.home_team: 0}

        self.batting = self.home_team
        self.throwing = self.away_team

        self.half = 0
        self.change = True
        self.outs = 0

        self.pitch = 0
        self.balls = 0
        self.strikes = 0
        self.inplay = False
        self.score = False

        self.bases = [None, None, None]
        self.scored = []

    @staticmethod
    def _get_pitch_clazz(text):
        if 'Ball' in text:
            return 'success'
        if 'In play' in text:
            return 'primary'
        return 'danger'

    def create_pitch_row(self, text, tables):
        clazz = self._get_pitch_clazz(text)
        pill = '<div class="badge badge-pill pitch alert-{}">{}</div>'
        left = cell(content=(pill.format(clazz, self.pitch) + text))
        count = '{} - {}'.format(self.balls, self.strikes)
        if clazz == 'primary':
            right = cell()
        else:
            right = cell(content=span(classes=['text-secondary'], text=count))
        tables.append_body([left, right])

    def create_summary_row(self, tables):
        summary = tables.get_summary()
        for player in self.scored:
            summary.append('{} scores.'.format(player))
            self.runs[self.batting] += 1
            self.score = True
        self.scored = []

        content = player_to_name_sub(' '.join(summary))
        outs = 'out' in content and 'advances to 1st' not in content

        if self.inplay:
            runs = 'scores' in content
            text = 'In play, '
            text += 'run(s)' if runs else 'out(s)' if outs else 'no out'
            self.handle_pitch_strike()
            self.create_pitch_row(text, tables)

        if outs:
            content += ' <b>{}</b>'.format(self.to_outs_str())
        if self.score:
            classes = ['badge', 'border', 'tag', 'tag-light']
            content += '&nbsp;&nbsp;'
            content += span(classes=classes, text=self.to_score_str())
            self.score = False

        tables.append_body([cell(col=col(colspan='2'), content=content)])

    def get_change_inning(self):
        return self.change

    def get_runner(self, base):
        return self.bases[base - 1]

    def handle_batter_to_base(self, batter, base):
        for i in range(min(3, base), 0, -1):
            if self.bases[i - 1]:
                self.handle_runner_to_base(self.bases[i - 1], base + 1)
                self.bases[i - 1] = None
        if base == 4:
            self.runs[self.batting] += 1
            self.score = True
        else:
            self.bases[base - 1] = batter

    def handle_change_batter(self):
        self.pitch = 0
        self.balls = 0
        self.strikes = 0
        self.inplay = False
        self.score = False

    def handle_change_inning(self):
        self.batting, self.throwing = self.throwing, self.batting
        self.half += 1
        self.change = False
        self.outs = 0
        self.bases = [None, None, None]

    def handle_change_runner(self, base, runner):
        self.bases[base - 1] = runner

    def handle_out_batter(self):
        self.handle_out()

    def handle_out_runner(self, base):
        self.handle_out()
        self.bases[base - 1] = None

    def handle_out(self):
        self.outs += 1

    def handle_pitch_ball(self):
        self.handle_pitch()
        self.balls += 1

    def handle_pitch_foul(self):
        self.handle_pitch()
        self.strikes = min(2, self.strikes + 1)

    def handle_pitch_strike(self):
        self.handle_pitch()
        self.strikes += 1

    def handle_pitch(self):
        self.pitch += 1

    def handle_runner_to_base(self, player, base):
        if base > 3:
            self.scored.append(player)
            return
        elif self.bases[base - 1]:
            self.handle_runner_to_base(self.bases[base - 1], base + 1)
        self.bases[base - 1] = player

    def is_strikeout(self):
        return self.strikes == 3

    def is_walk(self):
        return self.balls == 4

    def set_change_inning(self):
        self.change = True

    def set_inplay(self):
        self.inplay = True

    def to_bases_str(self):
        first, second, third = self.bases
        if first and second and third:
            return 'Bases loaded'
        if first and second:
            return 'Runners on 1st and 2nd'
        if first and third:
            return 'Runners on 1st and 3rd'
        if second and third:
            return 'Runners on 2nd and 3rd'
        if first:
            return 'Runner on 1st'
        if second:
            return 'Runner on 2nd'
        if third:
            return 'Runner on 3rd'
        return 'Bases empty'

    def to_head_str(self):
        return '{} &nbsp;|&nbsp; {}, {}'.format(self.to_score_str(),
                                                self.to_bases_str(),
                                                self.to_outs_str())

    def to_inning_str(self):
        s = 'Top' if self.half % 2 == 1 else 'Bottom'
        n = (self.half + 1) // 2
        return '{} {}{}'.format(s, n, suffix(n))

    def to_outs_str(self):
        return '{} out'.format(self.outs)

    def to_score_str(self):
        s = '{} {} · {} {}'.format(
            self.away_team,
            self.runs[self.away_team],
            self.home_team,
            self.runs[self.home_team],
        )
        return encoding_to_abbreviation_sub(s)


def create_state(data):
    return State(data)
