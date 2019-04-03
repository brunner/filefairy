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

EVENT_CHANGES = [
    Event.CHANGE_INNING,
    Event.CHANGE_BATTER,
    Event.CHANGE_FIELDER,
    Event.CHANGE_PINCH_HITTER,
    Event.CHANGE_PINCH_RUNNER,
    Event.CHANGE_PITCHER,
]

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

SMALLCAPS = {k: v for k, v in zip('BCDFHLPRS', 'ʙᴄᴅꜰʜʟᴘʀs')}


def _advance(bases, scored, player, base):
    if base > 2:
        scored.append(player)
        return
    elif bases[base]:
        _advance(bases, scored, bases[base], base + 1)
    bases[base] = player


def _base(bases, scored, player, base):
    for i in range(base, -1, -1):
        if bases[i]:
            _advance(bases, scored, bases[i], base + 1)
            bases[i] = None
    bases[base] = player


def _play(text, runs):
    content = player_to_name_sub(text)
    return [cell(col=col(colspan='2'), content=content)]


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

    def createBatterTable(self, body):
        clazz = 'border mb-3'
        hc = [col(colspan='2', clazz='font-weight-bold text-dark')]
        bc = [col(), col(clazz='text-right w-50p')]
        head = [[cell(content=self.toHeadStr())]]
        body.append(self.createPlayerRow(False))
        body.append(self.createPlayerRow(True))
        return table(clazz=clazz, hcols=hc, bcols=bc, head=head, body=body)

    def createPlayerRow(self, bats):
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

    def createPitchBallRow(self):
        return self.createPitchRow('success', 'Ball')

    def createPitchCalledStrikeRow(self):
        return self.createPitchRow('danger', 'Called Strike')

    def createPitchRow(self, clazz, text):
        pill = '<div class="badge badge-pill pitch alert-{}">{}</div>'
        left = cell(content=(pill.format(clazz, self.pitch) + text))
        count = '{} - {}'.format(self.balls, self.strikes)
        right = cell(content=span(classes=['text-secondary'], text=count))
        return [left, right]

    def createBattingSubstitutionRow(self, batter):
        title = 'Offensive Substitution'
        text = 'Pinch hitter: {}'.format(batter)
        return self.createSubstitutionRow(title, text)

    def createFieldingSubstitutionRow(self, position, player):
        title = 'Defensive Substitution'
        text = 'Now in {}: {}'.format(position, player)
        return self.createSubstitutionRow(title, text)

    def createPitchingSubstitutionRow(self, pitcher):
        title = 'Pitching Substitution'
        text = '{} replaces {}.'.format(pitcher, self.pitchers[self.throwing])
        return self.createSubstitutionRow(title, text)

    def createRunningSubstitutionRow(self, base, player):
        title = 'Offensive Substitution'
        text = 'Pinch runner at {}: {}'.format(base, player)
        return self.createSubstitutionRow(title, text)

    def createSubstitutionRow(self, title, text):
        content = player_to_name_sub('<b>{}</b><br>{}'.format(title, text))
        return [cell(col=col(colspan='2'), content=content)]

    def createSummaryRow(self, summary):
        content = player_to_name_sub(' '.join(summary))
        if 'out' in content:
            content += ' <b>{}</b>'.format(self.toOutsStr())
        return [cell(col=col(colspan='2'), content=content)]

    def getBatter(self):
        return self.batter

    def getChangeInning(self):
        return self.change

    def getColors(self):
        return self.colors

    def getPitcher(self):
        return self.pitcher

    def handleChangeBatter(self, batter):
        self.batter = batter
        self.pitch = 0
        self.balls = 0
        self.strikes = 0

    def handleChangeInning(self):
        self.half += 1
        self.change = False
        self.batting, self.throwing = self.throwing, self.batting
        self.batter = None
        self.pitcher = self.pitchers[self.throwing]
        self.outs = 0
        self.bases = [None, None, None]

    def handleChangePitcher(self, pitcher):
        self.pitcher = pitcher
        self.pitchers[self.throwing] = pitcher

    def handlePitcherBall(self):
        self.pitch += 1
        self.balls += 1

    def handlePitcherStrike(self):
        self.pitch += 1
        self.strikes += 1

    def isChangePitcher(self, pitcher):
        return pitcher != self.pitcher

    def setChangeInning(self):
        self.change = True

    def toBasesStr(self):
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

    def toHeadStr(self):
        return '{} &nbsp;|&nbsp; {}, {}'.format(self.toScoreStr(),
                                                self.toBasesStr(),
                                                self.toOutsStr())

    def toInningStr(self):
        s = 'Top' if self.half % 2 == 1 else 'Bottom'
        n = (self.half + 1) // 2
        return '{} {}{}'.format(s, n, suffix(n))

    def toOutsStr(self):
        return '{} out'.format(self.outs)

    def toScoreStr(self):
        s = '{} {} · {} {}'.format(
            self.away_team,
            self.runs[self.away_team],
            self.home_team,
            self.runs[self.home_team],
        )
        return encoding_to_abbreviation_sub(s)


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

    colors = state.getColors()
    jerseys = [(encoding, colors[encoding]) for encoding in colors]
    styles = call_service('uniforms', 'jersey_style', (*jerseys, ))

    t, body, post, tables = table(), [], [], []
    for group in _group(data['events']):
        summary = []
        for encoding in group:
            e, args = Event.decode(encoding)
            if e == Event.CHANGE_INNING:
                state.setChangeInning()
                continue
            elif state.getChangeInning():
                state.handleChangeInning()
                tables.append(topper(state.toInningStr()))

            if e in [Event.CHANGE_BATTER, Event.CHANGE_PINCH_HITTER]:
                batter, = args
                if e == Event.CHANGE_PINCH_HITTER:
                    body.append(state.createBattingSubstitutionRow(batter))
                state.handleChangeBatter(*args)
                t, body = state.createBatterTable(body), []
                tables.append(t)
                continue
            if e == Event.CHANGE_FIELDER:
                body.append(state.createFieldingSubstitutionRow(*args))
            if e == Event.CHANGE_PINCH_RUNNER:
                body.append(state.createRunningSubstitutionRow(*args))
            if e == Event.CHANGE_PITCHER:
                pitcher, = args
                if state.isChangePitcher(pitcher):
                    body.append(state.createPitchingSubstitutionRow(pitcher))
                    state.handleChangePitcher(pitcher)
                continue

            if summary and e in EVENT_PITCHES:
                body.append(state.createSummaryRow(summary))

            if e == Event.PITCHER_BALL:
                state.handlePitcherBall()
                body.append(state.createPitchBallRow())
            if e in [
                    Event.PITCHER_STRIKE_CALL,
                    Event.PITCHER_STRIKE_CALL_TOSSED,
            ]:
                state.handlePitcherStrike()
                body.append(state.createPitchCalledStrikeRow())
            #     if strikes == 3:
            #         outs += 1
            #         summary.append('{} called out on strikes.'.format(batter))
            #     if e == Event.PITCHER_STRIKE_CALL_TOSSED:
            #         _title = 'Ejection'
            #         _text = '{} ejected for arguing the call.'.format(batter)
            #         post.append(_change(_title, _text))
            # if e == Event.PITCHER_STRIKE_FOUL:
            #     pitch, strikes = pitch + 1, min(2, strikes + 1)
            #     _row = _pitch('danger', pitch, balls, strikes, 'Foul Ball')
            #     body.append(_row)
            # if e == Event.PITCHER_STRIKE_SWING:
            #     pitch, strikes = pitch + 1, strikes + 1
            #     _text = 'Swinging Strike'
            #     _row = _pitch('danger', pitch, balls, strikes, _text)
            #     body.append(_row)
            #     if strikes == 3:
            #         outs += 1
            #         summary.append('{} strikes out swinging.'.format(batter))

            # if e in [Event.BATTER_SINGLE, Event.BATTER_SINGLE_INFIELD]:
            #     _base(bases, scored, batter, 0)
            #     summary.append('{} singles.'.format(batter))
            # if e == Event.BATTER_SINGLE_APPEAL:
            #     _base(bases, scored, batter, 0)
            #     bases[0] = None
            #     outs += 1
            #     summary.append(
            #         '{} singles. Batter out on appeal for missing first base.'.
            #         format(batter))
            # if e == Event.BATTER_SINGLE_BATTED_OUT:
            #     _base(bases, scored, batter, 0)
            #     outs += 1
            #     summary.append(
            #         '{} singles. Runner out being hit by batted ball.'.format(
            #             batter))
            # if e == Event.BATTER_SINGLE_BUNT:
            #     _base(bases, scored, batter, 0)
            #     summary.append('{} singles on a bunt.'.format(batter))
            # if e == Event.BATTER_SINGLE_ERR:
            #     _base(bases, scored, batter, 1)
            #     summary.append(
            #         '{} singles. Error in OF, batter to second base.')
            # if e == Event.BATTER_SINGLE_STRETCH:
            #     _base(bases, scored, batter, 1)
            #     bases[1] = None
            #     outs += 1
            #     summary.append(
            #         '{} singles. Batter out at second base trying to stretch hit.'
            #         .format(batter))

        if summary:
            body.append(state.createSummaryRow(summary))
        for _row in body:
            tbody(t, _row)
        for _row in post:
            tbody(t, _row)
        body, post = [], []

    return {'styles': styles, 'tables': tables}
