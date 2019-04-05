#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for displaying live sim data."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/livesim', '', _path))

from common.datetime_.datetime_ import suffix  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import tbody  # noqa
from common.elements.elements import topper  # noqa
from common.json_.json_ import loads  # noqa
from common.reference.reference import player_to_bats  # noqa
from common.reference.reference import player_to_name  # noqa
from common.reference.reference import player_to_name_sub  # noqa
from common.reference.reference import player_to_number  # noqa
from common.reference.reference import player_to_throws  # noqa
from common.service.service import call_service  # noqa
from common.teams.teams import encoding_to_abbreviation_sub  # noqa
from common.teams.teams import encoding_to_nickname  # noqa
from data.event.event import Event  # noqa

SMALLCAPS = {k: v for k, v in zip('BCDFHLPRS', 'ʙᴄᴅꜰʜʟᴘʀs')}


def get_base(base):
    if base == 'F':
        return 1
    if base == 'S':
        return 2
    if base == 'T':
        return 3


def get_outcome(path, out):
    if out:
        if path == 'F':
            return 'flies out'
        if path == 'G':
            return 'grounds out'
        if path == 'L':
            return 'lines out'
        return 'pops out'
    if path == 'F':
        return 'fly ball'
    if path == 'G':
        return 'ground ball'
    if path == 'L':
        return 'line drive'
    return 'pop up'


def get_position(zone, outfield):
    if outfield:
        if '8' in zone or 'M' in zone:
            return 'CF'
        if '3' in zone or '4' in zone or '9' in zone:
            return 'RF'
        return 'LF'
    if '1' in zone or 'P' in zone:
        return 'P'
    if '2' in zone:
        return 'C'
    if '3' in zone:
        return '1B'
    if '5' in zone:
        return '3B'
    if '4' in zone:
        return '2B'
    if '7' in zone:
        return 'LF'
    if '8' in zone:
        return 'CF'
    if '9' in zone:
        return 'RF'
    return 'SS'


def get_title(position):
    if position == 'P':
        return 'pitcher'
    if position == 'C':
        return 'catcher'
    if position == '1B':
        return 'first baseman'
    if position == '2B':
        return 'second baseman'
    if position == '3B':
        return 'third baseman'
    if position == 'SS':
        return 'shortstop'
    if position == 'LF':
        return 'left fielder'
    if position == 'CF':
        return 'center fielder'
    if position == 'RF':
        return 'right fielder'


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
                index = len(lineups)
                fielders[curr] = player
                lineups.append([player])
                self.batters[player] = [curr, change.strip(','), index, None]
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
        _1, change, index, prev = self.batters[batter]
        curr, change = (change + ',').split(',', 1)
        self.batters[batter] = [curr, change, index, prev]
        self.lineups[self.batting][index].insert(0, batter)

        title = 'Offensive Substitution'
        text = 'Pinch hitter {} replaces {}.'.format(batter, prev)
        return self.create_titled_row(title, text)

    def create_change_fielder_row(self, position, player):
        title = 'Defensive Substitution'
        text = 'Now in {}: {}'.format(position, player)
        return self.create_titled_row(title, text)

    def create_change_pitcher_row(self, pitcher):
        title = 'Pitching Substitution'
        text = '{} replaces {}.'.format(pitcher, self.get_pitcher())
        return self.create_titled_row(title, text)

    def create_change_runner_row(self, runner):
        _, change, index, prev = self.batters[runner]
        curr, change = (change + ',').split(',', 1)
        self.batters[runner] = [curr, change, index, prev]
        self.lineups[self.batting][index].insert(0, runner)

        title = 'Offensive Substitution'
        text = 'Pinch runner {} replaces {}.'.format(runner, prev)
        return self.create_titled_row(title, text)

    def create_titled_row(self, title, text):
        content = player_to_name_sub('<b>{}</b><br>{}'.format(title, text))
        return [cell(col=col(colspan='2'), content=content)]

    def get_batter(self):
        return self.lineups[self.batting][self.get_index()][0]

    def get_fielder(self, position):
        player = self.fielders[self.throwing][position]
        return get_title(position) + ' ' + player

    def get_index(self):
        return self.indices[self.batting]

    def get_pitcher(self):
        return self.pitchers[self.throwing][0]

    def get_styles(self):
        jerseys = [(team, self.colors[team]) for team in self.colors]
        return call_service('uniforms', 'jersey_style', (*jerseys, ))

    def handle_change_batter(self):
        self.indices[self.batting] = (self.get_index() + 1) % 9

    def handle_change_inning(self):
        self.batting, self.throwing = self.throwing, self.batting

    def handle_change_pitcher(self, pitcher):
        self.pitchers[self.throwing].insert(0, pitcher)
        self.fielders[self.throwing]['P'] = pitcher
        if pitcher in self.batters:
            _, change, index, prev = self.batters[pitcher]
            curr, change = (change + ',').split(',', 1)
            self.batters[pitcher] = [curr, change, index, prev]
            self.lineups[self.throwing][index].insert(0, pitcher)

    def is_change_pitcher(self, pitcher):
        return pitcher != self.get_pitcher()


class State(object):
    def __init__(self, data):
        self.away_team = data['away_team']
        self.home_team = data['home_team']

        self.runs = {self.away_team: 0, self.home_team: 0}

        self.half = 0
        self.change = True
        self.outs = 0

        self.pitch = 0
        self.balls = 0
        self.strikes = 0
        self.inplay = False

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
        content = player_to_name_sub(' '.join(tables.get_summary()))
        outs = 'out' in content and 'advances to 1st' not in content

        if self.inplay:
            runs = 'scores' in content
            text = 'In play, '
            text += 'run(s)' if runs else 'out(s)' if outs else 'no out'
            self.handle_pitch_strike()
            self.create_pitch_row(text, tables)

        if outs:
            content += ' <b>{}</b>'.format(self.to_outs_str())

        tables.append_body([cell(col=col(colspan='2'), content=content)])

    def get_change_inning(self):
        return self.change

    def get_runner(self, base):
        return self.bases[base - 1]

    def handle_batter_to_base(self, batter, base):
        for i in range(base, 0, -1):
            if self.bases[i - 1]:
                self.handle_runner_to_base(self.bases[i - 1], base + 1)
                self.bases[i - 1] = None
        self.bases[base - 1] = batter

    def handle_change_batter(self):
        self.pitch = 0
        self.balls = 0
        self.strikes = 0
        self.inplay = False

    def handle_change_inning(self):
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


class Tables(object):
    def __init__(self):
        self.body = []
        self.foot = []
        self.summary = []
        self.table = table()
        self.tables = []

    def append_all(self):
        for row in self.body:
            tbody(self.table, row)
        for row in self.foot:
            tbody(self.table, row)

    def append_foot(self, row):
        self.foot.append(row)

    def append_body(self, row):
        self.body.append(row)

    def append_summary(self, s):
        self.summary.append(s)

    def append_table(self, table_):
        self.table = table_
        self.tables.append(table_)

    def create_table(self, roster, state):
        clazz = 'border mb-3'
        hcols = [col(colspan='2', clazz='font-weight-bold text-dark')]
        bcols = [col(), col(clazz='text-right w-50p')]
        head = [[cell(content=state.to_head_str())]]
        body, self.body = list(self.body), []

        self.body.append(roster.create_player_row(False))
        self.body.append(roster.create_player_row(True))
        self.table = table(
            clazz=clazz, hcols=hcols, bcols=bcols, head=head, body=body)
        self.tables.append(self.table)

    def get_body(self):
        return list(self.body)

    def get_summary(self):
        return list(self.summary)

    def get_tables(self):
        return self.tables

    def reset_all(self):
        self.body = []
        self.foot = []
        self.summary = []

    def reset_body(self):
        self.body = []

    def reset_summary(self):
        self.summary = []


EVENT_CHANGES = [
    Event.CHANGE_INNING,
    Event.CHANGE_BATTER,
    Event.CHANGE_FIELDER,
    Event.CHANGE_PINCH_HITTER,
    Event.CHANGE_PINCH_RUNNER,
    Event.CHANGE_PITCHER,
]


def _check_change_events(e, args, roster, state, tables):
    if e == Event.CHANGE_INNING:
        state.set_change_inning()
    elif state.get_change_inning():
        roster.handle_change_inning()
        state.handle_change_inning()
        tables.append_table(topper(state.to_inning_str()))

    if e in [Event.CHANGE_BATTER, Event.CHANGE_PINCH_HITTER]:
        roster.handle_change_batter()
        state.handle_change_batter()
        if e == Event.CHANGE_PINCH_HITTER:
            batter, = args
            tables.append_body(roster.create_change_batter_row(batter))
        tables.create_table(roster, state)
    if e == Event.CHANGE_FIELDER:
        position, player = args
        tables.append_body(roster.create_change_fielder_row(position, player))
    if e == Event.CHANGE_PINCH_RUNNER:
        base, runner = args
        state.handle_change_runner(get_base(base), runner)
        tables.append_body(roster.create_change_runner_row(runner))
    if e == Event.CHANGE_PITCHER:
        pitcher, = args
        if roster.is_change_pitcher(pitcher):
            tables.append_body(roster.create_change_pitcher_row(pitcher))
            roster.handle_change_pitcher(pitcher)


EVENT_SINGLE_BASES = [
    Event.BATTER_SINGLE,
    Event.BATTER_SINGLE_BATTED_OUT,
    Event.BATTER_SINGLE_BUNT,
    Event.BATTER_SINGLE_INFIELD,
    Event.BATTER_SINGLE_ERR,
    Event.BATTER_SINGLE_STRETCH,
]


def _check_single_base_events(e, args, roster, state, tables):
    batter = roster.get_batter()
    state.set_inplay()
    if e == Event.BATTER_SINGLE:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_fielder(get_position(zone, True))
        tables.append_summary('{} singles on a {} to {}.'.format(
            batter, outcome, fielder))
        state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_SINGLE_INFIELD:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_fielder(get_position(zone, False))
        tables.append_summary('{} singles on a {} to {}.'.format(
            batter, outcome, fielder))
        state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_SINGLE_BATTED_OUT:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_fielder(get_position(zone, False))
        tables.append_summary('{} singles on a {} to {}.'.format(
            batter, outcome, fielder))
        base = 1 if ('3' in zone or '4' in zone) else 2
        runner = state.get_runner(base)
        advance = '2nd' if base == 1 else '3rd'
        tables.append_summary('{} out at {} (hit by batted ball).'.format(
            runner, advance))
        state.handle_out_runner(base)
        state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_SINGLE_BUNT:
        zone, = args
        fielder = roster.get_fielder(get_position(zone, False))
        tables.append_summary('{} singles on a bunt ground ball to {}.'.format(
            batter, fielder))
        state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_SINGLE_ERR:
        scoring, path, _ = args
        outcome = get_outcome(path, False)
        fielder = roster.get_fielder(get_position(scoring, True))
        tables.append_summary('{} singles on a {} to {}.'.format(
            batter, outcome, fielder))
        tables.append_summary(
            '{} advances to 2nd, on a fielding error by {}.'.format(
                batter, fielder))
        state.handle_batter_to_base(batter, 2)
    if e == Event.BATTER_SINGLE_STRETCH:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_fielder(get_position(zone, False))
        receiver = roster.get_fielder('2B' if '7' in zone else 'SS')
        tables.append_summary('{} singles on a {} to {}.'.format(
            batter, outcome, fielder))
        tables.append_summary('{} out at {}{}, {} to {}.'.format(
            batter, 2, suffix(2), fielder, receiver))
        state.handle_batter_to_base(batter, 1)
        state.handle_out_runner(1)


EVENT_BATTED_OUTS = [
    Event.BATTER_FLY,
    Event.BATTER_FLY_BUNT,
    Event.BATTER_FLY_BUNT_DP,
    Event.BATTER_GROUND,
    Event.BATTER_GROUND_BUNT,
    Event.BATTER_GROUND_DP,
    Event.BATTER_GROUND_FC,
    Event.BATTER_GROUND_HOME,
    Event.BATTER_SINGLE_APPEAL,
    Event.BATTER_LINED_DP,
]


def _check_batted_out_events(e, args, roster, state, tables):
    batter = roster.get_batter()
    state.set_inplay()
    if e == Event.BATTER_FLY:
        scoring, path, _ = args
        outcome = get_outcome(path, True)
        fielder = roster.get_fielder(get_position(scoring, False))
        tables.append_summary('{} {} to {}.'.format(batter, outcome, fielder))
        state.handle_out_batter()
    if e == Event.BATTER_FLY_BUNT:
        _, scoring = args
        fielder = roster.get_fielder(get_position(scoring, False))
        tables.append_summary('{} bunt flies out to {}.'.format(
            batter, fielder))
        state.handle_out_batter()


EVENT_PITCHES = [
    Event.PITCHER_BALL,
    Event.PITCHER_WALK,
    Event.PITCHER_STRIKE_CALL,
    Event.PITCHER_STRIKE_CALL_TOSSED,
    Event.PITCHER_STRIKE_FOUL,
    Event.PITCHER_STRIKE_FOUL_BUNT,
    Event.PITCHER_STRIKE_FOUL_ERR,
    Event.PITCHER_STRIKE_MISS,
    Event.PITCHER_STRIKE_SWING,
    Event.PITCHER_STRIKE_SWING_OUT,
    Event.PITCHER_STRIKE_SWING_PASSED,
    Event.PITCHER_STRIKE_SWING_WILD,
]


def _check_pitch_events(e, args, roster, state, tables):
    if tables.get_summary():
        state.create_summary_row(tables)
        tables.reset_summary()

    batter = roster.get_batter()
    if e == Event.PITCHER_BALL:
        state.handle_pitch_ball()
        state.create_pitch_row('Ball', tables)
        if state.is_walk():
            tables.append_summary('{} walks.'.format(batter))
            state.handle_batter_to_base(batter, 1)
    if e == Event.PITCHER_WALK:
        pitcher = roster.get_pitcher()
        tables.append_summary('{} walked intentionally by {}.'.format(
            batter, pitcher))
        state.handle_batter_to_base(batter, 1)
    if e in [Event.PITCHER_STRIKE_CALL, Event.PITCHER_STRIKE_CALL_TOSSED]:
        state.handle_pitch_strike()
        state.create_pitch_row('Called Strike', tables)
        if state.is_strikeout():
            tables.append_summary('{} called out on strikes.'.format(batter))
            state.handle_out_batter()
        if e == Event.PITCHER_STRIKE_CALL_TOSSED:
            foot = roster.create_titled_row(
                'Ejection', '{} ejected for arguing the call.'.format(batter))
            tables.append_foot(foot)
    if e in [Event.PITCHER_STRIKE_FOUL, Event.PITCHER_STRIKE_FOUL_ERR]:
        state.handle_pitch_foul()
        state.create_pitch_row('Foul', tables)
        if e == Event.PITCHER_STRIKE_FOUL_ERR:
            scoring, = args
            fielder = roster.get_fielder(get_position(scoring, False))
            body = roster.create_titled_row(
                'Error', 'Dropped foul ball error by {}.'.format(fielder))
            tables.append_body(body)
    if e == Event.PITCHER_STRIKE_FOUL_BUNT:
        state.handle_pitch_strike()
        state.create_pitch_row('Foul Bunt', tables)
        if state.is_strikeout():
            tables.append_summary(
                '{} strikes out on a foul bunt.'.format(batter))
            state.handle_out_batter()
    if e == Event.PITCHER_STRIKE_MISS:
        state.handle_pitch_strike()
        state.create_pitch_row('Missed Bunt', tables)
        if state.is_strikeout():
            tables.append_summary(
                '{} strikes out on a missed bunt.'.format(batter))
            state.handle_out_batter()
    if e == Event.PITCHER_STRIKE_SWING:
        state.handle_pitch_strike()
        state.create_pitch_row('Swinging Strike', tables)
        if state.is_strikeout():
            tables.append_summary('{} strikes out swinging.'.format(batter))
            state.handle_out_batter()
    if e == Event.PITCHER_STRIKE_SWING_PASSED:
        state.handle_pitch_strike()
        state.create_pitch_row('Swinging Strike', tables)
        tables.append_summary('{} strikes out swinging.'.format(batter))
        fielder = roster.get_fielder('C')
        s = '{} advances to 1st, on a passed ball by {}.'.format(
            batter, fielder)
        tables.append_summary(s)
        state.handle_batter_to_base(batter, 1)
    if e == Event.PITCHER_STRIKE_SWING_WILD:
        state.handle_pitch_strike()
        state.create_pitch_row('Swinging Strike', tables)
        tables.append_summary('{} strikes out swinging.'.format(batter))
        fielder = roster.get_fielder('P')
        s = '{} advances to 1st, on a wild pitch by {}.'.format(
            batter, fielder)
        tables.append_summary(s)
        state.handle_batter_to_base(batter, 1)


def _group(encodings):
    change = None
    group = []
    for encoding in encodings:
        e, _ = Event.decode(encoding)
        c = e in EVENT_CHANGES
        if not group:
            change = c
            group.append(encoding)
        elif change == c:
            group.append(encoding)
        else:
            yield group
            change = c
            group = [encoding]

    if group:
        yield group


def get_html(game_in):
    """Gets template data for a given game data object.

    Args:
        game_in: The game data file path.

    Returns:
        The template data.
    """
    data = loads(game_in)
    if not data['events']:
        return None

    roster = Roster(data)
    state = State(data)
    tables = Tables()

    try:
        for group in _group(data['events']):
            for encoding in group:
                e, args = Event.decode(encoding)

                if e in EVENT_CHANGES:
                    _check_change_events(e, args, roster, state, tables)
                if e in EVENT_SINGLE_BASES:
                    _check_single_base_events(e, args, roster, state, tables)
                if e in EVENT_BATTED_OUTS:
                    _check_batted_out_events(e, args, roster, state, tables)
                if e in EVENT_PITCHES:
                    _check_pitch_events(e, args, roster, state, tables)

            if tables.get_summary():
                state.create_summary_row(tables)
                tables.reset_summary()

            tables.append_all()
            tables.reset_all()
    except Exception as e:
        print(game_in)
        raise e

    styles = roster.get_styles()
    return {'styles': styles, 'tables': tables.get_tables()}
