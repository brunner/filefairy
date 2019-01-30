#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data (non-reloadable) object for game event codes."""

import logging
from enum import IntEnum
from enum import auto

_logger = logging.getLogger('filefairy')


def _transform(s):
    if s in ['first', 'First', '1st']:
        return 'F'
    if s in ['second', 'Second', '2nd']:
        return 'S'
    if s in ['third', 'Third', '3rd']:
        return 'T'
    if s in ['home']:
        return 'H'

    return s


class Event(IntEnum):
    """Describe a number of different types of events that happen in a game.

    Attributes:
        base: A base name for the event. For example, `S` for second base.
        distance: A batted ball's travel distance. For example, `402`.
        path: A batted ball's flight path. For example, `F` for a fly ball.
        player: A player that the event describes. For example, `P24322`.
        position: A fielder position. For example, `LF`.
        runs: A number of runs that a team has at the end of an inning.
        scoring: A scoring notation for the event. For example, `4-3`.
        zone: A batted ball's location. For example, `7LD`.
    """
    CHANGE_INNING = auto()  # [runs, runs]

    CHANGE_BATTER = auto()  # [player]
    CHANGE_FIELDER = auto()  # [position, player]
    CHANGE_PINCH_HITTER = auto()  # [player]
    CHANGE_PINCH_RUNNER = auto()  # [num, player]
    CHANGE_PITCHER = auto()  # [player]

    BATTER_SINGLE = auto()  # [path, zone]
    BATTER_SINGLE_APPEAL = auto()  # []
    BATTER_SINGLE_BUNT = auto()  # [zone]
    BATTER_SINGLE_INFIELD = auto()  # [path, zone]
    BATTER_SINGLE_ERR = auto()  # [scoring, path, zone]

    BATTER_DOUBLE = auto()  # [path, zone]
    BATTER_TRIPLE = auto()  # [path, zone]
    BATTER_HOME_RUN = auto()  # [path, zone, distance]

    BATTER_REACH_DROPPED = auto()  # [position, scoring, zone]
    BATTER_REACH_FIELDING = auto()  # [scoring, path, zone]

    BATTER_FLY = auto()  # [scoring, path, zone]
    BATTER_FLY_BUNT = auto()  # [zone, scoring]
    BATTER_FLY_BUNT_DP = auto()  # [zone, name, scoring]

    BATTER_GROUND = auto()  # [scoring, zone]
    BATTER_GROUND_BUNT = auto()  # [zone, scoring]
    BATTER_GROUND_DP = auto()  # [scoring, zone]
    BATTER_GROUND_FC = auto()  # [num, scoring, zone]
    BATTER_GROUND_HOME = auto()  # [scoring, zone]

    BATTER_SAC_BUNT = auto()  # [zone, scoring]
    BATTER_SAC_BUNT_DP = auto()  # []
    BATTER_SAC_BUNT_OUT = auto()  # [zone, name, scoring]
    BATTER_SAC_BUNT_SAFE = auto()  # [zone, scoring]

    CATCHER_PASSED_BALL = auto()  # []
    CATCHER_PICK_OUT = auto()  # [base]
    FIELDER_THROWING = auto()  # [scoring]
    PITCHER_PICK_ERR = auto()  # []
    PITCHER_PICK_OUT = auto()  # []

    PITCHER_BALK = auto()  # []
    PITCHER_HIT_BY_PITCH = auto()  # []
    PITCHER_WILD_PITCH = auto()  # []

    PITCHER_BALL = auto()  # []
    PITCHER_WALK = auto()  # []

    PITCHER_STRIKE_CALL = auto()  # []
    PITCHER_STRIKE_FOUL = auto()  # []
    PITCHER_STRIKE_FOUL_BUNT = auto()  # []
    PITCHER_STRIKE_FOUL_ERR = auto()  # [scoring]
    PITCHER_STRIKE_MISS = auto()  # []

    PITCHER_STRIKE_SWING = auto()  # []
    PITCHER_STRIKE_SWING_OUT = auto()  # []
    PITCHER_STRIKE_SWING_PASSED = auto()  # []
    PITCHER_STRIKE_SWING_WILD = auto()  # []

    RUNNER_STEAL = auto()  # [player, num]
    RUNNER_STEAL_OUT = auto()  # [player, num, scoring]
    RUNNER_STEAL_THROWING = auto()  # [player, num]

    PLAYER_MOVE = auto()  # [player, name]
    PLAYER_SCORE = auto()  # [player]

    BASE_MOVE = auto()  # [num]
    BASE_MOVE_THROW = auto()  # [num]
    BASE_OUT = auto()  # [num, scoring]
    BASE_SCORE = auto()  # []
    BASE_SCORE_THROW = auto()  # []
    BASE_SCORE_TRAIL = auto()  # []
    BASE_SCORE_TRAIL_OUT = auto()  # [scoring]

    PARSE_ERROR = auto()  # []

    NONE = auto()  # []

    @classmethod
    def decode(cls, encoding):
        try:
            if ' ' in encoding:
                data = encoding.split(' ')
                return (cls[data[0].upper()], data[1:])
            return (cls[encoding.upper()], [])
        except Exception as e:
            _logger.log(logging.WARNING, 'Handled warning.', exc_info=True)
            return (None, [])

    def encode(self, *args):
        return ' '.join([self.name.lower()] + [_transform(s) for s in args])
