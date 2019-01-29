#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data (non-reloadable) object for game event codes."""

import os
import re
import sys
from enum import auto

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/event', '', _path))

from data.enum_.enum_ import Enum  # noqa


class Event(Enum):
    """Describe a number of different types of events that happen in a game.

    Attributes:
        base: A base name for the event. For example, `S` for second base.
        distance: A batted ball's travel distance. For example, `402`.
        name: A base name for the event. For example, `s` for second base.
        num: A base number for the event. For example, `1` for first base.
        path: A batted ball's flight path. For example, `F` for a fly ball.
        player: A player that the event describes. For example, `P24322`.
        position: A fielder position. For example, `LF`.
        scoring: A scoring notation for the event. For example, `4-3`.
        zone: A batted ball's location. For example, `7LD`.
    """
    CHANGE_INNING = auto()  # []

    CHANGE_BATTER = auto()  # [player]
    CHANGE_FIELDER = auto()  # [position, player]
    CHANGE_PINCH_HITTER = auto()  # [player]
    CHANGE_PINCH_RUNNER = auto()  # [num, player]
    CHANGE_PITCHER = auto()  # [player]

    BATTER_SINGLE = auto()  # [path, zone]
    BATTER_SINGLE_APPEAL = auto()  # []
    BATTER_SINGLE_BUNT = auto()  # [zone]
    BATTER_SINGLE_INFIELD = auto()  # [path, zone]
    BATTER_SINGLE_ERROR = auto()  # [scoring, path, zone]

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
    PITCHER_PICK_ERROR = auto()  # []
    PITCHER_PICK_OUT = auto()  # []

    PITCHER_BALK = auto()  # []
    PITCHER_HIT_BY_PITCH = auto()  # []
    PITCHER_WILD_PITCH = auto()  # []

    PITCHER_BALL = auto()  # []
    PITCHER_WALK = auto()  # []

    PITCHER_STRIKE_CALL = auto()  # []
    PITCHER_STRIKE_FOUL = auto()  # []
    PITCHER_STRIKE_FOUL_BUNT = auto()  # []
    PITCHER_STRIKE_FOUL_ERROR = auto()  # [scoring]
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

    NONE = auto()  # []
