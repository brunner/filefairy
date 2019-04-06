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
                curr, change = (pos + ',').split(',', 1)
                i = len(lineups)
                fielders[curr] = player
                lineups.append([player])
                self.batters[player] = [curr, change.strip(','), i, None]
            for line in data[team + '_bench']:
                player, pos, _, prev = line.split()
                self.batters[player] = [None, pos, self.batters[prev][2], prev]
            if 'P' not in fielders:
                fielders['P'] = data[team + '_pitcher']

        self.pitchers = {}
        self.pitchers[self.away_team] = [data['away_pitcher']]
        self.pitchers[self.home_team] = [data['home_pitcher']]

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
        args = (team, self.colors[team], num, 'back')
        img = call_service('uniforms', 'jersey_absolute', args)
        spn = span(classes=['profile-text', 'align-middle', 'd-block'], text=s)
        inner = img + spn

        content = '<div class="position-relative h-58p">{}</div>'.format(inner)
        return [cell(col=col(colspan='2'), content=content)]

    def create_change_batter_row(self, batter):
        _1, change, i, prev = self.batters[batter]
        curr, change = (change + ',').split(',', 1)
        self.batters[batter] = [curr, change, i, prev]
        self.lineups[self.batting][i].insert(0, batter)

        bold = 'Offensive Substitution'
        text = 'Pinch hitter {} replaces {}.'.format(batter, prev)
        return self.create_bolded_row(bold, text)

    def create_change_runner_row(self, runner):
        _, change, i, prev = self.batters[runner]
        curr, change = (change + ',').split(',', 1)
        self.batters[runner] = [curr, change, i, prev]
        self.lineups[self.batting][i].insert(0, runner)

        bold = 'Offensive Substitution'
        text = 'Pinch runner {} replaces {}.'.format(runner, prev)
        return self.create_bolded_row(bold, text)

    def create_bolded_row(self, title, text):
        content = player_to_name_sub('<b>{}</b><br>{}'.format(title, text))
        return [cell(col=col(colspan='2'), content=content)]

    def get_batter(self):
        return self.lineups[self.batting][self.get_index()][0]

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

    def handle_change_batter(self):
        self.indices[self.batting] = (self.get_index() + 1) % 9

    def handle_change_fielder(self, player, tables):
        curr, change, i, prev = self.batters[player]
        position, change = (change + ',').split(',', 1)

        if curr is None:
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
                player, get_written(position))
            return self.create_bolded_row(bold, text)
        else:
            bold = 'Defensive Switch'
            text = 'Defensive switch from {} to {} for {}.'.format(
                get_written(curr), get_written(position), player)
            return self.create_bolded_row(bold, text)

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
        bold = 'Pitching Substitution'
        if pitcher in self.batters:
            _, change, i, prev = self.batters[pitcher]
            curr, change = (change + ',').split(',', 1)
            title = get_title(self.batters[prev][0])
            title = title + ' ' if title else ''
            text = '{} replaces {}, batting {}{}, replacing {}{}.'.format(
                pitcher, self.get_pitcher(), i + 1, suffix(i + 1), title, prev)
            tables.append_body(self.create_bolded_row(bold, text))
            self.batters[pitcher] = [curr, change, i, prev]
            self.lineups[self.throwing][i].insert(0, pitcher)
        else:
            text = '{} replaces {}.'.format(pitcher, self.get_pitcher())
            tables.append_body(self.create_bolded_row(bold, text))

        self.pitchers[self.throwing].insert(0, pitcher)
        self.fielders[self.throwing]['P'] = pitcher

    def is_change_pitcher(self, pitcher):
        return pitcher != self.get_pitcher()


def create_roster(data):
    return Roster(data)
