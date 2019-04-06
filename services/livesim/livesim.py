#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for displaying live sim data."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/livesim', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import tbody  # noqa
from common.elements.elements import topper  # noqa
from common.events.events import get_bag  # noqa
from common.events.events import get_base  # noqa
from common.events.events import get_outcome  # noqa
from common.events.events import get_position  # noqa
from common.events.events import get_seats  # noqa
from common.json_.json_ import loads  # noqa
from common.service.service import call_service  # noqa
from data.event.event import Event  # noqa


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
        _, player = args
        roster.handle_change_fielder(player, tables)
    if e == Event.CHANGE_PINCH_RUNNER:
        base, runner = args
        state.handle_change_runner(get_base(base), runner)
        tables.append_body(roster.create_change_runner_row(runner))
    if e == Event.CHANGE_PITCHER:
        pitcher, = args
        if roster.is_change_pitcher(pitcher):
            roster.handle_change_pitcher(pitcher, tables)


EVENT_BATTER_REACHES = [
    Event.BATTER_SINGLE,
    Event.BATTER_SINGLE_BATTED_OUT,
    Event.BATTER_SINGLE_BUNT,
    Event.BATTER_SINGLE_INFIELD,
    Event.BATTER_SINGLE_ERR,
    Event.BATTER_SINGLE_STRETCH,
    Event.BATTER_DOUBLE,
    Event.BATTER_DOUBLE_STRETCH,
    Event.BATTER_TRIPLE,
    Event.BATTER_HOME_RUN,
    Event.BATTER_HOME_RUN_INSIDE,
    Event.BATTER_REACH_DROPPED,
    Event.BATTER_REACH_FIELDING,
    Event.BATTER_REACH_INTERFERENCE,
]


def _check_batter_reach_events(e, args, roster, state, tables):
    batter = roster.get_batter()
    state.set_inplay()
    if e == Event.BATTER_SINGLE:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_title_fielder(get_position(zone, True))
        tables.append_summary('{} singles on a {} to {}.'.format(
            batter, outcome, fielder))
        state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_SINGLE_INFIELD:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_title_fielder(get_position(zone, False))
        tables.append_summary('{} singles on a {} to {}.'.format(
            batter, outcome, fielder))
        state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_SINGLE_BATTED_OUT:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_title_fielder(get_position(zone, False))
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
        fielder = roster.get_title_fielder(get_position(zone, False))
        tables.append_summary('{} singles on a bunt ground ball to {}.'.format(
            batter, fielder))
        state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_SINGLE_ERR:
        scoring, path, _ = args
        outcome = get_outcome(path, False)
        fielder = roster.get_title_fielder(get_position(scoring, True))
        tables.append_summary('{} singles on a {} to {}.'.format(
            batter, outcome, fielder))
        tables.append_summary(
            '{} advances to 2nd, on a fielding error by {}.'.format(
                batter, fielder))
        state.handle_batter_to_base(batter, 2)
    if e == Event.BATTER_SINGLE_STRETCH:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_title_fielder(get_position(zone, False))
        receiver = roster.get_title_fielder('2B' if '7' in zone else 'SS')
        tables.append_summary('{} singles on a {} to {}.'.format(
            batter, outcome, fielder))
        tables.append_summary('{} out at 2nd, {} to {}.'.format(
            batter, fielder, receiver))
        state.handle_batter_to_base(batter, 2)
        state.handle_out_runner(2)
    if e == Event.BATTER_DOUBLE:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_title_fielder(get_position(zone, True))
        tables.append_summary('{} doubles on a {} to {}.'.format(
            batter, outcome, fielder))
        state.handle_batter_to_base(batter, 2)
    if e == Event.BATTER_DOUBLE_STRETCH:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_title_fielder(get_position(zone, False))
        receiver = roster.get_title_fielder('3B')
        tables.append_summary('{} doubles on a {} to {}.'.format(
            batter, outcome, fielder))
        tables.append_summary('{} out at 3rd, {} to {}.'.format(
            batter, fielder, receiver))
        state.handle_batter_to_base(batter, 3)
        state.handle_out_runner(3)
    if e == Event.BATTER_TRIPLE:
        path, zone = args
        outcome = get_outcome(path, False)
        fielder = roster.get_title_fielder(get_position(zone, True))
        tables.append_summary('{} triples on a {} to {}.'.format(
            batter, outcome, fielder))
        state.handle_batter_to_base(batter, 3)
    if e == Event.BATTER_HOME_RUN:
        path, zone, distance = args
        outcome = get_outcome(path, False)
        tables.append_summary('{} homers on a {} to {} ({} ft).'.format(
            batter, outcome, get_seats(zone), distance))
        state.handle_batter_to_base(batter, 4)
    if e == Event.BATTER_HOME_RUN_INSIDE:
        path, zone = args
        outcome = get_outcome(path, False)
        tables.append_summary(
            '{} hits an inside-the-park home run on a {} to {}.'.format(
                batter, outcome, get_seats(zone)))
        state.handle_batter_to_base(batter, 4)
    if e == Event.BATTER_REACH_DROPPED:
        position, scoring, _ = args
        fielder = roster.get_title_fielder(position)
        receiver = roster.get_title_fielder(get_position(scoring, False))
        tables.append_summary(
            '{} reaches on a missed catch error by {}, assist to {}.'.format(
                batter, receiver, fielder))
        state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_REACH_FIELDING:
        scoring, _1, _2 = args
        fielder = roster.get_title_fielder(get_position(scoring, False))
        tables.append_summary('{} reaches on a fielding error by {}.'.format(
            batter, fielder))
        state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_REACH_INTERFERENCE:
        fielder = roster.get_fielder('C')
        tables.append_summary(
            '{} reaches on catcher interference by {}.'.format(
                batter, fielder))
        state.handle_batter_to_base(batter, 1)


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
        fielder = roster.get_title_fielder(get_position(scoring, False))
        tables.append_summary('{} {} to {}.'.format(batter, outcome, fielder))
        state.handle_out_batter()
    if e == Event.BATTER_FLY_BUNT:
        _, scoring = args
        fielder = roster.get_title_fielder(get_position(scoring, False))
        tables.append_summary('{} bunt flies out to {}.'.format(
            batter, fielder))
        state.handle_out_batter()
    if e == Event.BATTER_FLY_BUNT_DP:
        _1, _2, scoring = args
        base = 1 if scoring[-1] == '3' else 3 if scoring[-1] == '5' else 2
        runner = state.get_runner(base)
        tables.append_summary('{} bunt lines into a double play, {}.'.format(
            batter, roster.get_scoring(scoring)))
        tables.append_summary('{} out at {}.'.format(runner, get_bag(base)))
        state.handle_out_batter()
        state.handle_out_runner(base)
    if e in [Event.BATTER_GROUND, Event.BATTER_GROUND_BUNT]:
        scoring, _ = args
        outcome = 'bunt ' if e == Event.BATTER_GROUND_BUNT else ''
        outcome += 'grounds out'
        tables.append_summary('{} {}, {}.'.format(batter, outcome,
                                                  roster.get_scoring(scoring)))
        state.handle_out_batter()
    if e == Event.BATTER_GROUND_DP:
        scoring, _ = args
        i = 1 if scoring[0] == 'U' else 2
        base = 3 if scoring[i] == '2' else 2 if scoring[i] == '5' else 1
        runner = state.get_runner(base)
        tables.append_summary('{} grounds into a double play, {}.'.format(
            batter, roster.get_scoring(scoring)))
        tables.append_summary('{} out at {}.'.format(runner,
                                                     get_bag(base + 1)))
        state.handle_out_batter()
        state.handle_out_runner(base)
    if e == Event.BATTER_GROUND_FC:
        base, scoring, _ = args
        base = get_base(base)
        runner = state.get_runner(base - 1)
        tables.append_summary('{} grounds into a force out, {}.'.format(
            batter, roster.get_scoring(scoring)))
        tables.append_summary('{} out at {}.'.format(runner, get_bag(base)))
        state.handle_batter_to_base(batter, 1)
        state.handle_out_runner(base)
    if e == Event.BATTER_GROUND_HOME:
        scoring, _ = args
        runner = state.get_runner(3)
        tables.append_summary('{} grounds into a force out, {}.'.format(
            batter, roster.get_scoring(scoring)))
        tables.append_summary('{} out at home.'.format(runner))
        state.handle_out_runner(3)
        state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_SINGLE_APPEAL:
        tables.append_summary('{} grounds out, {}.'.format(
            batter, roster.get_scoring('U3')))
        state.handle_out_batter()
    if e == Event.BATTER_LINED_DP:
        scoring, _1, _2 = args
        i = 1 if scoring[0] == 'U' else 2
        base = 1 if scoring[i] == '3' else 3 if scoring[i] == '5' else 2
        runner = state.get_runner(base)
        tables.append_summary('{} out at {}, {}.'.format(
            runner, get_bag(base), roster.get_scoring(scoring)))
        state.handle_out_runner(base)


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
            foot = roster.create_bolded_row(
                'Ejection', '{} ejected for arguing the call.'.format(batter))
            tables.append_foot(foot)
    if e in [Event.PITCHER_STRIKE_FOUL, Event.PITCHER_STRIKE_FOUL_ERR]:
        state.handle_pitch_foul()
        state.create_pitch_row('Foul', tables)
        if e == Event.PITCHER_STRIKE_FOUL_ERR:
            scoring, = args
            fielder = roster.get_title_fielder(get_position(scoring, False))
            body = roster.create_bolded_row(
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
        fielder = roster.get_title_fielder('C')
        s = '{} advances to 1st, on a passed ball by {}.'.format(
            batter, fielder)
        tables.append_summary(s)
        state.handle_batter_to_base(batter, 1)
    if e == Event.PITCHER_STRIKE_SWING_WILD:
        state.handle_pitch_strike()
        state.create_pitch_row('Swinging Strike', tables)
        tables.append_summary('{} strikes out swinging.'.format(batter))
        fielder = roster.get_title_fielder('P')
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

    roster = call_service('roster', 'create_roster', (data, ))
    state = call_service('state', 'create_state', (data, ))
    tables = call_service('tables', 'create_tables', ())

    try:
        for group in _group(data['events']):
            for encoding in group:
                e, args = Event.decode(encoding)

                if e in EVENT_CHANGES:
                    _check_change_events(e, args, roster, state, tables)
                if e in EVENT_BATTER_REACHES:
                    _check_batter_reach_events(e, args, roster, state, tables)
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
