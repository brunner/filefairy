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
from common.elements.elements import icon_img  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.re_.re_ import search  # noqa
from common.reference.reference import player_to_name_sub  # noqa
from common.teams.teams import encoding_to_abbreviation_sub  # noqa
from common.teams.teams import encoding_to_decoding_sub  # noqa
from common.teams.teams import encoding_to_hometown_sub  # noqa

HLEFTCLZ = 'font-weight-bold text-dark text-dark w-95p'
HMIDCLZ = 'font-weight-bold text-dark text-truncate text-center '
HMEDCLZ = HMIDCLZ + 'td-md-show'
HLONGCLZ = HMIDCLZ + 'td-md-none'
HRIGHTCLZ = HLEFTCLZ + ' text-right'
HEADCLZ = 'table-fixed border border-bottom-0'

ICON_LINK = 'https://fairylab.surge.sh/images/bases/{}.png'


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
        self.souts = 0

        self.pitch = 0
        self.balls = 0
        self.strikes = 0
        self.inplay = False
        self.score = False

        self.bases = [None, None, None]
        self.scored = []

    @staticmethod
    def _get_pitch_clazz(text):
        if 'Ball' in text or 'Hit By Pitch' in text:
            return 'success'
        if 'In play' in text:
            return 'primary'
        return 'danger'

    def create_head_table(self):
        hcols = [
            col(clazz=HLEFTCLZ),
            col(clazz=HMEDCLZ),
            col(clazz=HLONGCLZ),
            col(clazz=HRIGHTCLZ)
        ]
        right = '{} &nbsp; {}'.format(self.to_outs_str(), self.to_bases_str())
        head = [[
            cell(content=self.to_inning_str(True)),
            cell(content=self.to_score_medium_str()),
            cell(content=self.to_score_long_str()),
            cell(content=right)
        ]]
        return table(clazz=HEADCLZ, hcols=hcols, head=head)

    def create_pitch_row(self, text, tables):
        clazz = self._get_pitch_clazz(text)
        pill = '<div class="badge badge-pill pitch alert-{}">{}</div>'
        left = cell(content=(pill.format(clazz, self.pitch) + text))
        count = '{} - {}'.format(self.balls, self.strikes)
        if clazz == 'primary':
            right = cell()
        else:
            right = cell(content=span(classes=['text-secondary'], text=count))
        tables.append_old_body([left, right])

    def create_summary_row(self, tables):
        summary = tables.get_summary()
        for player in self.scored:
            summary.append('{} scores.'.format(player))
            self.runs[self.batting] += 1
            self.score = True
        self.scored = []

        end, players = [], set()
        for s in ['scores', 'home', '3rd', '2nd', '1st']:
            lines, summary = list(summary), []
            safe = r' scores\.' if s == 'scores' else r' to {}\.'.format(s)
            out = r' out at {}'.format(s)
            for line in lines:
                regex = r'(P\d+)(?:{}|{})'.format(safe, out)
                player = search(regex, line)
                if player:
                    if player in players:
                        continue
                    end.append(line)
                    players.add(player)
                else:
                    summary.append(line)

        content = ' '.join(summary + end)

        outs = self.souts != self.outs
        self.souts = self.outs

        if self.inplay:
            runs = search(r'(?: scores\.| homers )', content)
            text = 'In play, '
            text += 'run(s)' if runs else 'out(s)' if outs else 'no out'
            self.handle_pitch_strike()
            self.create_pitch_row(text, tables)

            advances = search(r' (?:scores|to 3rd|to 2nd)\.', content)
            if advances and not search(r' error', content):
                content = re.sub(r'(?:flies|lines|pops) out',
                                 r'out on a sacrifice fly', content)

        if outs:
            content += ' <b>{}</b>'.format(self.to_outs_str())
        if self.score:
            ac = ['badge', 'border', 'tag', 'tag-light']
            before = span(classes=['before-score'], text=content)
            after = span(classes=ac, text=self.to_score_short_str())
            content = before + after
            self.score = False

        content = player_to_name_sub(content)
        tables.append_old_body([cell(col=col(colspan='2'), content=content)])

    def get_change_inning(self):
        return self.change

    def get_outs(self):
        return self.outs

    def get_runner(self, base):
        return self.bases[base - 1]

    def get_runs_away(self):
        return self.runs[self.away_team]

    def get_runs_home(self):
        return self.runs[self.home_team]

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
        self.souts = 0
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
            if player not in self.scored:
                self.scored.append(player)
        else:
            if self.bases[base - 1] and self.bases[base - 1] != player:
                self.handle_runner_to_base(self.bases[base - 1], base + 1)
            self.bases[base - 1] = player
        for i in range(min(3, base - 1), 0, -1):
            if self.bases[i - 1] == player:
                self.bases[i - 1] = None

    def is_strikeout(self):
        return self.strikes == 3

    def is_walk(self):
        return self.balls == 4

    def set_change_inning(self):
        self.outs = 3
        self.bases = [None, None, None]
        self.change = True

    def set_inplay(self):
        self.inplay = True

    def set_runs(self, aruns, hruns):
        self.runs = {self.away_team: aruns, self.home_team: hruns}

    def to_bases_str(self):
        s = ''.join('x' if b else 'o' for b in self.bases)
        return icon_img(ICON_LINK.format(s), '16', None)

    def to_inning_str(self, start):
        if start:
            s = 'Top' if self.half % 2 == 1 else 'Bottom'
        else:
            s = 'Mid' if self.half % 2 == 1 else 'End'
        n = (self.half + 1) // 2
        return '{} {}{}'.format(s, n, suffix(n))

    def to_outs_str(self):
        return '{} out'.format(self.outs)

    def to_score_long_str(self):
        return self.to_score_str(encoding_to_decoding_sub, '{} {}, {} {}')

    def to_score_medium_str(self):
        return self.to_score_str(encoding_to_hometown_sub, '{} {}, {} {}')

    def to_score_short_str(self):
        return self.to_score_str(encoding_to_abbreviation_sub, '{} {} · {} {}')

    def to_score_str(self, f, s):
        args = (self.away_team, self.runs[self.away_team], self.home_team,
                self.runs[self.home_team])
        return f(s.format(*args))


def create_state(data):
    return State(data)
