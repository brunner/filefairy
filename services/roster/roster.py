#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for storing gameday player information."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/roster', '', _path))

from common.datetime_.datetime_ import suffix  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.events.events import get_position  # noqa
from common.events.events import get_title  # noqa
from common.events.events import get_written  # noqa
from common.math.math import crange  # noqa
from common.reference.reference import player_to_bats  # noqa
from common.reference.reference import player_to_name  # noqa
from common.reference.reference import player_to_name_sub  # noqa
from common.reference.reference import player_to_number  # noqa
from common.reference.reference import player_to_throws  # noqa
from common.service.service import call_service  # noqa

SMALLCAPS = {k: v for k, v in zip('BCDFHLPRS', 'ʙᴄᴅꜰʜʟᴘʀs')}


class Roster(object):
    def __init__(self, data):
        self.away_team = data['away_team']
        self.home_team = data['home_team']

        self.colors = {}
        self.colors[self.away_team] = data['away_colors'].split()
        self.colors[self.home_team] = data['home_colors'].split()

        self.batting = self.home_team
        self.throwing = self.away_team

        self.batters = {}
        self.indices = {self.away_team: 8, self.home_team: 8}
        self.fielders = {self.away_team: {}, self.home_team: {}}
        self.lineups = {self.away_team: [], self.home_team: []}
        for team in ['away', 'home']:
            encoding = data[team + '_team']
            fielders = self.fielders[encoding]
            lineups = self.lineups[encoding]
            for line in data[team + '_batting']:
                player, pos, _ = line.split()
                curr, change = self.pop_change(pos)
                i = len(lineups)
                fielders[curr] = player
                lineups.append([player])
                self.batters[player] = [curr, change, i, None]
            for line in data[team + '_bench']:
                player, pos, _, prev = line.split()
                self.batters[player] = [None, pos, self.batters[prev][2], prev]
            if 'P' not in fielders:
                fielders['P'] = data[team + '_pitcher']

        self.pitchers = {}
        self.pitchers[self.away_team] = [data['away_pitcher']]
        self.pitchers[self.home_team] = [data['home_pitcher']]

        self.injuries = data['injuries']

    def create_player_row(self, bats):
        team = self.batting if bats else self.throwing
        player = self.get_batter() if bats else self.get_pitcher()
        title = 'ᴀᴛ ʙᴀᴛ' if bats else 'ᴘɪᴛᴄʜɪɴɢ'
        hand = player_to_bats(player) if bats else player_to_throws(player)
        name = player_to_name(player)
        num = player_to_number(player)
        if bats:
            curr = self.batters[player][0]
            pos = ''.join(SMALLCAPS.get(c, c) for c in curr) + ' '
        else:
            pos = ''
        stats = ''

        s = '{}: {}#{} ({})<br>{}<br>{}'
        s = s.format(title, pos, num, SMALLCAPS.get(hand, 'ʀ'), name, stats)
        return self.create_jersey_row(team, num, 'back', s)

    def create_due_up_row(self):
        due = []
        i = self.get_index()
        for j in crange((i + 1) % 9, (i + 3) % 9, 9):
            due.append(self.get_batter_at(j))

        s = 'ᴅᴜᴇ ᴜᴘ:<br>{}<br>'.format(player_to_name_sub(', '.join(due)))
        return self.create_jersey_row(self.batting, None, 'front', s)

    def create_jersey_row(self, team, num, side, s):
        args = (team, self.colors[team], num, side)
        img = call_service('uniforms', 'jersey_absolute', args)
        spn = span(classes=['profile-text', 'align-middle', 'd-block'], text=s)
        inner = img + spn

        content = '<div class="position-relative h-58p">{}</div>'.format(inner)
        return [cell(col=col(colspan='2'), content=content)]

    def create_bolded_row(self, title, text):
        content = player_to_name_sub('<b>{}</b><br>{}'.format(title, text))
        return [cell(col=col(colspan='2'), content=content)]

    def get_batter_at(self, i):
        return self.lineups[self.batting][i][0]

    def get_batter(self):
        return self.get_batter_at(self.get_index())

    def get_fielder(self, position):
        return self.fielders[self.throwing][position]

    def get_index(self):
        return self.indices[self.batting]

    def get_pitcher(self):
        return self.pitchers[self.throwing][0]

    def get_scoring(self, scoring):
        zones = scoring.replace('U', '').split('-')
        zones = [self.get_title_fielder(get_position(z, False)) for z in zones]

        if len(zones) > 1:
            return ' to '.join(zones)
        return zones[0] + ' unassisted'

    def get_styles(self):
        jerseys = [(team, self.colors[team]) for team in self.colors]
        return call_service('uniforms', 'jersey_style', (*jerseys, ))

    def get_title_fielder(self, position):
        return get_title(position) + ' ' + self.get_fielder(position)

    def handle_change_batter(self, batter, tables):
        start = (self.get_index() + 1) % 9
        end = (start + 8) % 9
        for i in crange(start, end, 9):
            if batter == self.get_batter_at(i):
                self.indices[self.batting] = i
                break
        else:
            _1, change, i, prev = self.batters[batter]
            curr, change = self.pop_change(change)
            self.batters[batter] = [curr, change, i, prev]
            self.lineups[self.batting][i].insert(0, batter)
            self.indices[self.batting] = i
            self.handle_possible_injury(prev, tables)
            bold = 'Offensive Substitution'
            text = 'Pinch hitter {} replaces {}.'.format(batter, prev)
            tables.append_body(self.create_bolded_row(bold, text))

    def handle_change_fielder(self, player, tables):
        curr, change, i, prev = self.batters[player]
        position, change = self.pop_change(change)

        if curr is None:
            self.handle_possible_injury(prev, tables)
            bold = 'Defensive Substitution'
            title = get_title(self.batters[prev][0])
            title = title + ' ' if title else ''
            text = '{} replaces {}{}, batting {}{}, playing {}.'.format(
                player, title, prev, i + 1, suffix(i + 1),
                get_written(position))
            tables.append_body(self.create_bolded_row(bold, text))
        elif curr == 'PH' or curr == 'PR':
            bold = 'Defensive Switch'
            text = '{} remains in the game as the {}.'.format(
                player, get_title(position))
            tables.append_body(self.create_bolded_row(bold, text))
        else:
            bold = 'Defensive Switch'
            text = 'Defensive switch from {} to {} for {}.'.format(
                get_title(curr), get_title(position), player)
            tables.append_body(self.create_bolded_row(bold, text))

        self.batters[player] = [position, change, i, prev]
        self.lineups[self.throwing][i].insert(0, player)

        fielder = self.fielders[self.throwing][position]
        _1, _2, j, _3 = self.batters[fielder]
        if self.lineups[self.throwing][j][0] == fielder:
            self.handle_change_fielder(fielder, tables)

        self.fielders[self.throwing][position] = player

    def handle_change_inning(self):
        self.batting, self.throwing = self.throwing, self.batting

    def handle_change_pitcher(self, pitcher, tables):
        prev = self.get_pitcher()
        self.handle_possible_injury(prev, tables)

        bold = 'Pitching Substitution'
        if pitcher in self.batters:
            _, change, i, prev = self.batters[pitcher]
            curr, change = self.pop_change(change)
            title = get_title(self.batters[prev][0])
            title = title + ' ' if title else ''
            text = '{} replaces {}, batting {}{}, replacing {}{}.'.format(
                pitcher, prev, i + 1, suffix(i + 1), title, prev)
            tables.append_body(self.create_bolded_row(bold, text))
            self.batters[pitcher] = [curr, change, i, prev]
            self.lineups[self.throwing][i].insert(0, pitcher)
        else:
            text = '{} replaces {}.'.format(pitcher, prev)
            tables.append_body(self.create_bolded_row(bold, text))

        self.pitchers[self.throwing].insert(0, pitcher)
        self.fielders[self.throwing]['P'] = pitcher

    def handle_change_runner(self, runner, tables):
        _, change, i, prev = self.batters[runner]
        if change.startswith('PR,'):
            curr, change = self.pop_change(change)
        else:
            curr = 'PR'
        self.batters[runner] = [curr, change, i, prev]
        self.lineups[self.batting][i].insert(0, runner)
        self.handle_possible_injury(prev, tables)
        bold = 'Offensive Substitution'
        text = 'Pinch runner {} replaces {}.'.format(runner, prev)
        tables.append_body(self.create_bolded_row(bold, text))

    def handle_possible_injury(self, player, tables):
        if player in self.injuries:
            bold = 'Injury Delay'
            text = '{} was injured {}.'.format(player, self.injuries[player])
            tables.append_body(self.create_bolded_row(bold, text))

    def is_change_pitcher(self, pitcher):
        return pitcher != self.get_pitcher()

    def pop_change(self, change):
        curr, change = (change + ',').split(',', 1)
        return (curr, change.strip(','))


def create_roster(data):
    return Roster(data)
