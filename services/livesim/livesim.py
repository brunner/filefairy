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


def _fielders(data, team):
    fielders = {}
    for line in data[team + '_batting']:
        player, position, _ = line.split()
        position = position.split(',')[0]
        fielders[position] = player
    if 'P' not in fielders:
        fielders['P'] = data[team + '_pitcher']
    return fielders


def _players(data):
    players = {}
    for team in ['away', 'home']:
        for line in data[team + '_batting']:
            player, position, _ = line.split()
            players[player] = {'pos': position, 'prev': None}
        for line in data[team + '_bench']:
            player, position, _, prev = line.split()
            players[player] = {'pos': position, 'prev': prev}
    return players


LOCATIONS = {
    '1': ('P', 'pitcher'),
    '2': ('C', 'catcher'),
    '3': ('1B', 'first baseman'),
    '4': ('2B', 'second baseman'),
    '5': ('3B', 'third baseman'),
    '6': ('SS', 'shortstop'),
    '7': ('LF', 'left fielder'),
    '8': ('CF', 'center fielder'),
    '9': ('RF', 'right fielder')
}


def _location(zone, infield):
    if infield:
        if '1' in zone or 'P' in zone:
            return '1'
        if '2' in zone:
            return '2'
        if '3' in zone:
            return '3'
        if '5' in zone:
            return '5'
        if '4' in zone:
            return '4'
        return '6'
    else:
        if '8' in zone or 'M' in zone:
            return '8'
        if '3' in zone or '4' in zone or '9' in zone:
            return '9'
        return '7'


def _hit_path_str(path):
    if path == 'F':
        return 'fly ball'
    if path == 'G':
        return 'ground ball'
    if path == 'L':
        return 'line drive'
    return 'pop up'


def _out_path_str(path):
    if path == 'F':
        return 'flies out'
    if path == 'G':
        return 'grounds out'
    if path == 'L':
        return 'lines out'
    return 'pops out'


class State(object):
    def __init__(self, data):
        self.away_team = data['away_team']
        self.home_team = data['home_team']

        self.runs = {self.away_team: 0, self.home_team: 0}

        self.colors = {}
        self.colors[self.away_team] = data['away_colors'].split()
        self.colors[self.home_team] = data['home_colors'].split()

        self.pitchers = {}
        self.pitchers[self.away_team] = data['away_pitcher']
        self.pitchers[self.home_team] = data['home_pitcher']

        self.fielders = {}
        self.fielders[self.away_team] = _fielders(data, 'away')
        self.fielders[self.home_team] = _fielders(data, 'home')

        self.players = _players(data)

        self.batting = self.home_team
        self.throwing = self.away_team

        self.batter = None
        self.pitcher = self.pitchers[self.home_team]

        self.half = 0
        self.change = True
        self.outs = 0

        self.pitch = 0
        self.balls = 0
        self.strikes = 0

        self.bases = [None, None, None]
        self.scored = []

    @staticmethod
    def _get_pitch_clazz(text):
        if 'Ball' in text:
            return 'success'
        if 'In play' in text:
            return 'primary'
        return 'danger'

    def create_batter_table(self, tables):
        clazz = 'border mb-3'
        hc = [col(colspan='2', clazz='font-weight-bold text-dark')]
        bc = [col(), col(clazz='text-right w-50p')]
        head = [[cell(content=self.to_head_str())]]

        body = tables.get_body()
        body.append(self.create_player_row(False))
        body.append(self.create_player_row(True))

        table_ = table(clazz=clazz, hcols=hc, bcols=bc, head=head, body=body)
        tables.append_table(table_)
        tables.reset_body()

    def create_player_row(self, bats):
        team = self.batting if bats else self.throwing
        player = self.batter if bats else self.pitcher
        position = ''

        title = 'ᴀᴛ ʙᴀᴛ' if bats else 'ᴘɪᴛᴄʜɪɴɢ'
        hand = player_to_bats(player) if bats else player_to_throws(player)
        name = player_to_name(player)
        num = player_to_number(player)
        pos = ''.join(SMALLCAPS.get(c, c) for c in position)
        stats = ''

        s = '{}: {} #{} ({})<br>{}<br>{}'
        s = s.format(title, pos, num, SMALLCAPS.get(hand, 'ʀ'), name, stats)

        args = (team, self.colors[team], num, 'back')
        img = call_service('uniforms', 'jersey_absolute', args)
        spn = span(classes=['profile-text', 'align-middle', 'd-block'], text=s)
        inner = img + spn

        content = '<div class="position-relative h-58p">{}</div>'.format(inner)
        return [cell(col=col(colspan='2'), content=content)]

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

    def create_batting_substitution_row(self, args, tables):
        title = 'Offensive Substitution'
        text = 'Pinch hitter: {}'.format(*args)
        tables.append_body(self.create_titled_row(title, text))

    def create_fielding_substitution_row(self, args, tables):
        title = 'Defensive Substitution'
        text = 'Now in {}: {}'.format(*args)
        tables.append_body(self.create_titled_row(title, text))

    def create_pitching_substitution_row(self, args, tables):
        pitcher, = args
        title = 'Pitching Substitution'
        text = '{} replaces {}.'.format(pitcher, self.pitchers[self.throwing])
        tables.append_body(self.create_titled_row(title, text))

    def create_running_substitution_row(self, args, tables):
        title = 'Offensive Substitution'
        text = 'Pinch runner at {}: {}'.format(*args)
        tables.append_body(self.create_titled_row(title, text))

    def create_titled_row(self, title, text):
        content = player_to_name_sub('<b>{}</b><br>{}'.format(title, text))
        return [cell(col=col(colspan='2'), content=content)]

    def create_summary_row(self, tables):
        content = player_to_name_sub(' '.join(tables.get_summary()))
        outs = 'out' in content and 'advances to 1st' not in content

        if tables.is_inplay():
            runs = 'scores' in content
            text = 'In play, '
            text += 'run(s)' if runs else 'out(s)' if outs else 'no out'
            self.handle_pitch_strike()
            self.create_pitch_row(text, tables)

        if outs:
            content += ' <b>{}</b>'.format(self.to_outs_str())

        tables.append_body([cell(col=col(colspan='2'), content=content)])

    def get_batter(self):
        return self.batter

    def get_change_inning(self):
        return self.change

    def get_fielder(self, zone, infield):
        if zone is None:
            return None
        position, title = LOCATIONS[_location(zone, infield)]
        fielder = self.fielders[self.throwing][position]
        return title + ' ' + fielder

    def get_pitcher(self):
        return self.pitcher

    def get_runner(self, base):
        return self.bases[base - 1]

    def get_styles(self):
        jerseys = [(team, self.colors[team]) for team in self.colors]
        return call_service('uniforms', 'jersey_style', (*jerseys, ))

    def handle_batter_to_base(self, base):
        for i in range(base, 0, -1):
            if self.bases[i - 1]:
                self.handle_runner_to_base(self.bases[i - 1], base + 1)
                self.bases[i - 1] = None
        self.bases[base - 1] = self.batter

    def handle_change_batter(self, args):
        self.batter, = args
        self.pitch = 0
        self.balls = 0
        self.strikes = 0

    def handle_change_inning(self, tables):
        self.half += 1
        self.change = False
        self.batting, self.throwing = self.throwing, self.batting
        self.batter = None
        self.pitcher = self.pitchers[self.throwing]
        self.outs = 0
        self.bases = [None, None, None]
        tables.append_table(topper(self.to_inning_str()))

    def handle_change_pitcher(self, pitcher):
        self.pitcher = pitcher
        self.pitchers[self.throwing] = pitcher

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

    def is_change_pitcher(self, pitcher):
        return pitcher != self.pitcher

    def is_strikeout(self):
        return self.strikes == 3

    def is_walk(self):
        return self.balls == 4

    def set_change_inning(self):
        self.change = True

    def to_assist_out_str(self, runner, base, args):
        path, zone1 = args
        zone2 = '5' if base == 3 else '4' if '7' in zone1 else '6'
        fielder1 = self.get_fielder(zone1, False)
        fielder2 = self.get_fielder(zone2, True)
        return '{} out at {}{}, {} to {}.'.format(runner, base, suffix(base),
                                                  fielder1, fielder2)

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

    def to_hit_bunt_str(self, text, args):
        path, zone = args
        path = 'bunt ' + _hit_path_str(path)
        fielder = self.get_fielder(zone, True)
        return self.to_hit_str(text, path, fielder, zone)

    def to_hit_infield_str(self, text, args):
        path, zone = args
        path = _hit_path_str(path)
        fielder = self.get_fielder(zone, True)
        return self.to_hit_str(text, path, fielder, zone)

    def to_hit_outfield_str(self, text, args):
        path, zone = args
        path = _hit_path_str(path)
        fielder = self.get_fielder(zone, False)
        return self.to_hit_str(text, path, fielder, zone)

    def to_hit_str(self, text, path, fielder, zone):
        batter = self.get_batter()
        return '{} {} on a {} to {} (zone {}).'.format(batter, text, path,
                                                       fielder, zone)

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
        self.inplay = False
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

    def get_body(self):
        return list(self.body)

    def get_summary(self):
        return list(self.summary)

    def get_tables(self):
        return self.tables

    def is_inplay(self):
        return self.inplay

    def reset_all(self):
        self.body = []
        self.foot = []
        self.inplay = False
        self.summary = []

    def reset_body(self):
        self.body = []

    def reset_summary(self):
        self.summary = []

    def set_inplay(self):
        self.inplay = True


EVENT_CHANGES = [
    Event.CHANGE_INNING,
    Event.CHANGE_BATTER,
    Event.CHANGE_FIELDER,
    Event.CHANGE_PINCH_HITTER,
    Event.CHANGE_PINCH_RUNNER,
    Event.CHANGE_PITCHER,
]


def _check_change_events(e, args, state, tables):
    if e == Event.CHANGE_INNING:
        state.set_change_inning()
    elif state.get_change_inning():
        state.handle_change_inning(tables)

    if e in [Event.CHANGE_BATTER, Event.CHANGE_PINCH_HITTER]:
        if e == Event.CHANGE_PINCH_HITTER:
            state.create_batting_substitution_row(args, tables)
        state.handle_change_batter(args)
        state.create_batter_table(tables)
    if e == Event.CHANGE_FIELDER:
        state.create_fielding_substitution_row(args, tables)
    if e == Event.CHANGE_PINCH_RUNNER:
        state.create_running_substitution_row(args, tables)
    if e == Event.CHANGE_PITCHER:
        pitcher, = args
        if state.is_change_pitcher(pitcher):
            state.create_pitching_substitution_row(args, tables)
            state.handle_change_pitcher(pitcher)


EVENT_SINGLE_BASES = [
    Event.BATTER_SINGLE,
    Event.BATTER_SINGLE_BATTED_OUT,
    Event.BATTER_SINGLE_BUNT,
    Event.BATTER_SINGLE_INFIELD,
    Event.BATTER_SINGLE_ERR,
    Event.BATTER_SINGLE_STRETCH,
]


def _check_single_base_events(e, args, state, tables):
    batter = state.get_batter()
    tables.set_inplay()
    if e == Event.BATTER_SINGLE:
        tables.append_summary(state.to_hit_outfield_str('singles', args))
        state.handle_batter_to_base(1)
    if e == Event.BATTER_SINGLE_INFIELD:
        tables.append_summary(state.to_hit_infield_str('singles', args))
        state.handle_batter_to_base(1)
    if e == Event.BATTER_SINGLE_BATTED_OUT:
        path, zone = args
        tables.append_summary(state.to_hit_infield_str('singles', args))
        base = 1 if ('3' in zone or '4' in zone) else 2
        runner = state.get_runner(base)
        advance = '2nd' if base == 1 else '3rd'
        s = '{} out at {} (hit by batted ball).'.format(runner, advance)
        tables.append_summary(s)
        state.handle_out_runner(base)
        state.handle_batter_to_base(1)
    if e == Event.BATTER_SINGLE_BUNT:
        zone, = args
        args = ('G', zone)
        tables.append_summary(state.to_hit_bunt_str('singles', args))
        state.handle_batter_to_base(1)
    if e == Event.BATTER_SINGLE_ERR:
        scoring, path, zone = args
        args = (path, zone)
        fielder = state.get_fielder(scoring.strip('E'), False)
        tables.append_summary(state.to_hit_outfield_str('singles', args))
        s = '{} advances to 2nd, on a fielding error by {}.'.format(
            batter, fielder)
        tables.append_summary(s)
        state.handle_batter_to_base(2)
    if e == Event.BATTER_SINGLE_STRETCH:
        tables.append_summary(state.to_hit_outfield_str('singles', args))
        tables.append_summary(state.to_assist_out_str(batter, 2, args))
        state.handle_batter_to_base(1)
        state.handle_out_runner(1)


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


def _check_pitch_events(e, args, state, tables):
    if tables.get_summary():
        state.create_summary_row(tables)
        tables.reset_summary()

    batter = state.get_batter()
    if e == Event.PITCHER_BALL:
        state.handle_pitch_ball()
        state.create_pitch_row('Ball', tables)
        if state.is_walk():
            tables.append_summary('{} walks.'.format(batter))
            state.handle_batter_to_base(1)
    if e == Event.PITCHER_WALK:
        pitcher = state.get_pitcher()
        tables.append_summary('{} walked intentionally by {}.'.format(
            batter, pitcher))
        state.handle_batter_to_base(1)
    if e in [Event.PITCHER_STRIKE_CALL, Event.PITCHER_STRIKE_CALL_TOSSED]:
        state.handle_pitch_strike()
        state.create_pitch_row('Called Strike', tables)
        if state.is_strikeout():
            tables.append_summary('{} called out on strikes.'.format(batter))
            state.handle_out_batter()
        if e == Event.PITCHER_STRIKE_CALL_TOSSED:
            foot = state.create_titled_row(
                'Ejection', '{} ejected for arguing the call.'.format(batter))
            tables.append_foot(foot)
    if e in [Event.PITCHER_STRIKE_FOUL, Event.PITCHER_STRIKE_FOUL_ERR]:
        state.handle_pitch_foul()
        state.create_pitch_row('Foul', tables)
        if e == Event.PITCHER_STRIKE_FOUL_ERR:
            scoring, = args
            location = scoring.strip('E')
            fielder = state.get_fielder(location, int(location) < 7)
            body = state.create_titled_row(
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
        fielder = state.get_fielder('2', True)
        s = '{} advances to 1st, on a passed ball by {}.'.format(
            batter, fielder)
        tables.append_summary(s)
        state.handle_batter_to_base(1)
    if e == Event.PITCHER_STRIKE_SWING_WILD:
        state.handle_pitch_strike()
        state.create_pitch_row('Swinging Strike', tables)
        tables.append_summary('{} strikes out swinging.'.format(batter))
        fielder = state.get_fielder('1', True)
        s = '{} advances to 1st, on a wild pitch by {}.'.format(
            batter, fielder)
        tables.append_summary(s)
        state.handle_batter_to_base(1)


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

    state = State(data)
    tables = Tables()

    for group in _group(data['events']):
        for encoding in group:
            e, args = Event.decode(encoding)

            if e in EVENT_CHANGES:
                _check_change_events(e, args, state, tables)
            if e in EVENT_SINGLE_BASES:
                _check_single_base_events(e, args, state, tables)
            if e in EVENT_PITCHES:
                _check_pitch_events(e, args, state, tables)

        if tables.get_summary():
            state.create_summary_row(tables)
            tables.reset_summary()

        tables.append_all()
        tables.reset_all()

    styles = state.get_styles()
    return {'styles': styles, 'tables': tables.get_tables()}
