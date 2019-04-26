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
from common.elements.elements import row  # noqa
from common.events.events import get_bag  # noqa
from common.events.events import get_base  # noqa
from common.events.events import get_outcome  # noqa
from common.events.events import get_position  # noqa
from common.events.events import get_seats  # noqa
from common.json_.json_ import loads  # noqa
from common.reference.reference import player_to_name_sub  # noqa
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
        aruns, hruns = [int(a) for a in args]
        state.set_change_inning()
        if aruns != state.get_runs_away() or hruns != state.get_runs_home():
            state.set_runs(aruns, hruns)
            text = state.to_score_long_str()
            body = roster.create_bolded_row('Score Update', text)
            tables.append_old_body(body)
            tables.append_all()
            tables.reset_all()
    elif state.get_change_inning():
        roster.handle_change_inning()
        state.handle_change_inning(tables)

    if e in [Event.CHANGE_BATTER, Event.CHANGE_PINCH_HITTER]:
        batter, = args
        roster.handle_change_batter(batter, tables)
        state.handle_change_batter(tables)
        tables.create_old_table(roster, state)
    if e == Event.CHANGE_FIELDER:
        _, player = args
        roster.handle_change_fielder(player, tables)
    if e == Event.CHANGE_PINCH_RUNNER:
        base, runner = args
        roster.handle_change_runner(runner, tables)
        state.handle_change_runner(get_base(base), runner)
    if e == Event.CHANGE_PITCHER:
        pitcher, = args
        if roster.is_change_pitcher(pitcher):
            roster.handle_change_pitcher(pitcher, tables)


EVENT_BATTER_REACHES = [
    Event.BATTER_SINGLE,
    Event.BATTER_SINGLE_BATTED_OUT,
    Event.BATTER_SINGLE_BUNT,
    Event.BATTER_SAC_BUNT_HIT,
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
    if tables.get_summary():
        state.create_summary_row(tables)
        tables.reset_summary()

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
    if e in [Event.BATTER_SINGLE_BUNT, Event.BATTER_SAC_BUNT_HIT]:
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


EVENT_BATTER_OUTS = [
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
    Event.BATTER_SAC_BUNT,
    Event.BATTER_SAC_BUNT_DP,
    Event.BATTER_SAC_BUNT_OUT,
    Event.BATTER_SAC_BUNT_SAFE,
]


def _check_batter_out_events(e, args, roster, state, tables):
    if tables.get_summary():
        state.create_summary_row(tables)
        tables.reset_summary()

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
        state.handle_out_runner(base - 1)
        if state.get_outs() < 3:
            tables.append_summary('{} to {}.'.format(batter, get_bag(1)))
            state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_GROUND_HOME:
        scoring, _ = args
        runner = state.get_runner(3)
        tables.append_summary('{} grounds into a force out, {}.'.format(
            batter, roster.get_scoring(scoring)))
        tables.append_summary('{} out at home.'.format(runner))
        state.handle_out_runner(3)
        if state.get_outs() < 3:
            tables.append_summary('{} to {}.'.format(batter, get_bag(1)))
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
    if e == Event.BATTER_SAC_BUNT:
        _, scoring = args
        tables.append_summary('{} out on a sacrifice bunt, {}.'.format(
            batter, roster.get_scoring(scoring)))
        state.handle_batter_to_base(batter, 1)
        state.handle_out_runner(1)
    if e == Event.BATTER_SAC_BUNT_DP:
        base, _ = args
        base = get_base(base)
        scoring = '1-5-3' if base == 3 else '1-6-3'
        runner = state.get_runner(base - 1)
        tables.append_summary('{} bunt grounds into a double play, {}.'.format(
            batter, roster.get_scoring(scoring)))
        tables.append_summary('{} out at {}.'.format(runner, get_bag(base)))
        state.handle_out_batter()
        state.handle_out_runner(base - 1)
    if e == Event.BATTER_SAC_BUNT_OUT:
        _, base, scoring = args
        base = get_base(base)
        runner = state.get_runner(base - 1)
        tables.append_summary('{} bunt grounds into a force out, {}.'.format(
            batter, roster.get_scoring(scoring)))
        tables.append_summary('{} out at {}.'.format(runner, get_bag(base)))
        state.handle_out_runner(base - 1)
        if state.get_outs() < 3:
            tables.append_summary('{} to {}.'.format(batter, get_bag(1)))
            state.handle_batter_to_base(batter, 1)
    if e == Event.BATTER_SAC_BUNT_SAFE:
        _, base = args
        base = get_base(base)
        runner = state.get_runner(base - 1)
        tables.append_summary('{} hits a sacrifice bunt.'.format(batter))
        tables.append_summary('{} to {}.'.format(runner, get_bag(base)))
        tables.append_summary('{} to {}.'.format(batter, get_bag(1)))
        state.handle_runner_to_base(runner, base)
        state.handle_batter_to_base(batter, 1)


EVENT_MISC_BATTERS = [
    Event.CATCHER_PASSED_BALL,
    Event.CATCHER_PICK_ERR,
    Event.CATCHER_PICK_OUT,
    Event.FIELDER_THROWING,
    Event.PITCHER_PICK_ERR,
    Event.PITCHER_PICK_OUT,
    Event.PITCHER_BALK,
    Event.PITCHER_HIT_BY_PITCH,
    Event.PITCHER_HIT_BY_PITCH_CHARGE,
    Event.PITCHER_WILD_PITCH,
]


def _check_misc_batter_events(e, args, roster, state, tables):
    batter = roster.get_batter()
    pitcher = roster.get_pitcher()
    if e == Event.CATCHER_PASSED_BALL:
        tables.append_summary('With {} batting, passed ball by {}.'.format(
            batter, roster.get_title_fielder('C')))
    if e == Event.CATCHER_PICK_ERR:
        tables.append_summary(
            'With {} batting, throwing error by {} on the pickoff attempt.'.
            format(batter, roster.get_title_fielder('C')))
    if e == Event.CATCHER_PICK_OUT:
        base, = args
        base = get_base(base)
        runner = state.get_runner(base)
        position = '3B' if base == 3 else '1B' if base == 1 else 'SS'
        tables.append_summary(
            'With {} batting, {} picks off {} on throw to {}.'.format(
                batter, roster.get_title_fielder('C'), runner,
                roster.get_title_fielder(position)))
        state.handle_out_runner(base)
    if e == Event.FIELDER_THROWING:
        scoring, = args
        fielder = roster.get_title_fielder(get_position(scoring, False))
        tables.append_summary('Throwing error by {}.'.format(fielder))
    if e == Event.PITCHER_PICK_ERR:
        tables.append_summary(
            'With {} batting, throwing error by {} on the pickoff attempt.'.
            format(batter, pitcher))
    if e == Event.PITCHER_PICK_OUT:
        base, = args
        base = get_base(base)
        runner = state.get_runner(base)
        position = '3B' if base == 3 else '1B' if base == 1 else 'SS'
        tables.append_summary(
            'With {} batting, {} picks off {} on throw to {}.'.format(
                batter, pitcher, runner, roster.get_title_fielder(position)))
        state.handle_out_runner(base)
    if e == Event.PITCHER_BALK:
        tables.append_summary('With {} batting, balk by {}.'.format(
            batter, pitcher))
        for base in range(3, 0, -1):
            runner = state.get_runner(base)
            if runner:
                state.handle_runner_to_base(runner, base + 1)
                if base < 3:
                    tables.append_summary('{} to {}.'.format(
                        runner, get_bag(base + 1)))
    if e in [Event.PITCHER_HIT_BY_PITCH, Event.PITCHER_HIT_BY_PITCH_CHARGE]:
        state.handle_pitch_ball()
        state.create_pitch_row('Hit By Pitch', tables)
        tables.append_summary('{} hit by pitch.'.format(batter))
        state.handle_batter_to_base(batter, 1)
    if e == Event.PITCHER_WILD_PITCH:
        tables.append_summary('With {} batting, wild pitch by {}.'.format(
            batter, pitcher))


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
            tables.append_summary(
                '{} ejected for arguing the call.'.format(batter))
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
    if e == Event.PITCHER_STRIKE_SWING_OUT:
        state.handle_pitch_strike()
        state.create_pitch_row('Swinging Strike', tables)
        if state.is_strikeout():
            tables.append_summary('{} strikes out swinging, {}.'.format(
                batter, roster.get_scoring('2-3')))
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


EVENT_MISC_RUNNERS = [
    Event.RUNNER_STEAL,
    Event.RUNNER_STEAL_HOME,
    Event.RUNNER_STEAL_HOME_OUT,
    Event.RUNNER_STEAL_OUT,
    Event.RUNNER_STEAL_THROWING,
    Event.PLAYER_MOVE,
    Event.PLAYER_SCORE,
    Event.BASE_MOVE,
    Event.BASE_MOVE_RUNDOWN,
    Event.BASE_MOVE_THROW,
    Event.BASE_MOVE_TRAIL,
    Event.BASE_MOVE_TRAIL_OUT,
    Event.BASE_OUT,
    Event.BASE_SCORE,
    Event.BASE_SCORE_THROW,
    Event.BASE_SCORE_TRAIL,
    Event.BASE_SCORE_TRAIL_OUT,
]


def _check_misc_runner_events(e, args, roster, state, tables):
    batter = roster.get_batter()
    if e in [Event.RUNNER_STEAL, Event.RUNNER_STEAL_THROWING]:
        runner, base = args
        base = get_base(base)
        state.handle_runner_to_base(runner, base)
        tables.append_summary('With {} batting, {} steals {} base.'.format(
            batter, runner, get_bag(base)))
        if e == Event.RUNNER_STEAL_THROWING:
            tables.append_summary('Throwing error by {}.'.format(
                roster.get_title_fielder('C')))
    if e == Event.RUNNER_STEAL_HOME:
        runner, = args
        state.handle_runner_to_base(runner, 4)
        tables.append_summary('With {} batting, {} steals home.'.format(
            batter, runner, get_bag(base)))
        state.handle_runner_to_base(runner, 4)
    if e == Event.RUNNER_STEAL_HOME_OUT:
        runner, = args
        scoring = '1-2'
        state.handle_out_runner(3)
        tables.append_summary(
            'With {} batting, {} caught stealing home, {}.'.format(
                batter, runner, roster.get_scoring(scoring)))
    if e == Event.RUNNER_STEAL_OUT:
        runner, base, scoring = args
        base = get_base(base)
        state.handle_out_runner(base - 1)
        tables.append_summary(
            'With {} batting, {} caught stealing {} base, {}.'.format(
                batter, runner, get_bag(base), roster.get_scoring(scoring)))
    if e == Event.PLAYER_MOVE:
        runner, base = args
        base = get_base(base)
        state.handle_runner_to_base(runner, base)
        tables.append_summary('{} to {}.'.format(runner, get_bag(base)))
    if e == Event.PLAYER_SCORE:
        runner, = args
        state.handle_runner_to_base(runner, 4)
    if e in [Event.BASE_MOVE, Event.BASE_MOVE_RUNDOWN, Event.BASE_MOVE_THROW]:
        base, = args
        base = get_base(base)
        runner = state.get_runner(base)
        state.handle_runner_to_base(runner, base + 1)
        tables.append_summary('{} to {}.'.format(runner, get_bag(base + 1)))
    if e in [Event.BASE_MOVE_TRAIL, Event.BASE_MOVE_TRAIL_OUT]:
        runner = state.get_runner(2)
        state.handle_runner_to_base(runner, 3)
        tables.append_summary('{} to 3rd.'.format(runner))
        trailer = state.get_runner(1)
        if e == Event.BASE_MOVE_TRAIL:
            state.handle_runner_to_base(trailer, 2)
            tables.append_summary('{} to 2nd.'.format(trailer))
        else:
            scoring, = args
            state.handle_out_runner(1)
            tables.append_summary('{} out at 2nd on the throw, {}.'.format(
                trailer, roster.get_scoring(scoring)))
    if e == Event.BASE_OUT:
        base, scoring = args
        base = get_base(base)
        runner = state.get_runner(base)
        tables.append_summary('{} out at {} on the throw, {}.'.format(
            runner, get_bag(base + 1), roster.get_scoring(scoring)))
        state.handle_out_runner(base)
    if e in [Event.BASE_SCORE, Event.BASE_SCORE_THROW]:
        runner = state.get_runner(3)
        state.handle_runner_to_base(runner, 4)
    if e in [Event.BASE_SCORE_TRAIL, Event.BASE_SCORE_TRAIL_OUT]:
        runner = state.get_runner(3)
        state.handle_runner_to_base(runner, 4)
        trailer = state.get_runner(2)
        if e == Event.BASE_MOVE_TRAIL:
            state.handle_runner_to_base(trailer, 3)
            tables.append_summary('{} to 3rd.'.format(trailer))
        else:
            scoring, = args
            tables.append_summary('{} out at 3rd on the throw, {}.'.format(
                trailer, roster.get_scoring(scoring)))
            state.handle_out_runner(2)


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

    tables.append_live_head(roster.create_ballpark_table())
    tables.append_live_head(state.create_live_head_table())
    tables.append_live_head(roster.create_live_pitcher_table())
    tables.append_live_head(roster.create_live_batter_table())

    try:
        for group in _group(data['events']):
            for i, encoding in enumerate(list(group)):
                e, args = Event.decode(encoding)

                if e in EVENT_CHANGES:
                    _check_change_events(e, args, roster, state, tables)
                if e in EVENT_BATTER_REACHES:
                    _check_batter_reach_events(e, args, roster, state, tables)
                if e in EVENT_BATTER_OUTS:
                    _check_batter_out_events(e, args, roster, state, tables)
                if e in EVENT_MISC_BATTERS:
                    _check_misc_batter_events(e, args, roster, state, tables)
                if e in EVENT_PITCHES:
                    _check_pitch_events(e, args, roster, state, tables)
                if e in EVENT_MISC_RUNNERS:
                    _check_misc_runner_events(e, args, roster, state, tables)

                if e == Event.SPECIAL:
                    if tables.get_summary():
                        state.create_summary_row(tables)
                        tables.reset_summary()

                    body = roster.create_bolded_row(
                        'Parse Error', 'Unable to parse game event.')
                    tables.append_old_body(body)

                    text = player_to_name_sub(' '.join(args))
                    cells = [cell(col=col(colspan='2'), content=text)]
                    tables.append_old_body(row(cells=cells))

            if tables.get_summary():
                state.create_summary_row(tables)
                tables.reset_summary()

            tables.append_all()
            tables.reset_all()
    except Exception as e:
        print(game_in)
        raise e

    styles = roster.get_styles()
    tabs = [{
        'title': 'Live',
        'tables': tables.get_live_tables(),
    }, {
        'title': 'Box',
        'tables': [],
    }, {
        'title': 'Plays',
        'tables': [],
    }, {
        'title': 'Old',
        'tables': tables.get_old_tables(),
    }]
    return {'events': tables.get_live_events(), 'styles': styles, 'tabs': tabs}
