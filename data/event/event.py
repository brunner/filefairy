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
        base: A base for the event. For example, `1` for first base.
        distance: A batted ball's travel distance. For example, `402`.
        path: A batted ball's flight path. For example, `F` for a fly ball.
        player: A player that the event describes. For example, `P24322`.
        position: A fielder position. For example, `LF`.
        scoring: A scoring notation for the event. For example, `4-3`.
        zone: A batted ball's location. For example, `7LD`.
    """

    CHANGE_BATTER = auto()  # [player]
    CHANGE_FIELDER = auto()  # [position, player]
    CHANGE_INNING = auto()  # []
    CHANGE_PINCH_HITTER = auto()  # [player]
    CHANGE_PINCH_RUNNER = auto()  # [base, player]
    CHANGE_PITCHER = auto()  # [player]

    BATTER_INFIELD_SINGLE = auto()  # [path, zone]
    BATTER_SINGLE = auto()  # [path, zone]
    BATTER_DOUBLE = auto()  # [path, zone]
    BATTER_TRIPLE = auto()  # [path, zone]
    BATTER_HOME_RUN = auto()  # [path, zone, distance]
    BATTER_SINGLE_ERROR_IN_OUTFIELD = auto()  # [scoring, path, zone]
    BATTER_SINGLE_MISSED_BASE = auto()  # []

    BATTER_REACH_ON_DROPPED_THROW = auto()  # [position, scoring, zone]
    BATTER_REACH_ON_FIELDING_ERROR = auto()  # [scoring, path, zone]

    BATTER_BUNT_FLIES_INTO_DOUBLE_PLAY_AT_THIRD = auto()  # [zone, scoring]
    BATTER_BUNT_FLY_OUT = auto()  # [zone, scoring]
    BATTER_BUNT_GROUND_OUT = auto()  # [zone, scoring]
    BATTER_BUNT_HIT = auto()  # [zone]
    BATTER_FLY_OUT = auto()  # [scoring, path, zone]
    BATTER_GROUND_OUT = auto()  # [scoring, zone]
    BATTER_GROUNDS_INTO_DOUBLE_PLAY = auto()  # [scoring, zone]
    BATTER_GROUNDS_INTO_FIELDERS_CHOICE = auto()  # [scoring, zone]
    BATTER_SAC_BUNT_OUT_AT_FIRST = auto()  # [zone, scoring]
    BATTER_SAC_BUNT_OUT_AT_SECOND = auto()  # [zone, scoring]
    BATTER_SAC_BUNT_OUT_AT_SECOND_AT_FIRST = auto()  # []
    BATTER_SAC_BUNT_OUT_AT_THIRD = auto()  # [zone, scoring]
    BATTER_SAC_BUNT_SAFE_AT_FIRST = auto()  # [zone, scoring]
    BATTER_STRIKE_OUT = auto()

    CATCHER_PASSED_BALL = auto()  # []
    CATCHER_PICKOFF_FIRST_OUT = auto()  # []

    FIELDER_THROWING_ERROR = auto()  # [scoring]

    PITCHER_BALK = auto()  # []
    PITCHER_BALL = auto()  # []
    PITCHER_CALLED_STRIKE = auto()  # []
    PITCHER_FOULED_BUNT_STRIKE = auto()  # []
    PITCHER_FOULED_STRIKE = auto()  # []
    PITCHER_FOULED_STRIKE_WITH_ERROR = auto()  # [scoring]
    PITCHER_HIT_BY_PITCH = auto()  # []
    PITCHER_INTENTIONAL_WALK = auto()  # []
    PITCHER_MISSED_BUNT_STRIKE = auto()  # []
    PITCHER_PICKOFF_FIRST_ERROR = auto()  # []
    PITCHER_PICKOFF_FIRST_OUT = auto()  # []
    PITCHER_SWINGING_STRIKE = auto()  # []
    PITCHER_SWINGING_STRIKE_OUT_AT_FIRST = auto()  # []
    PITCHER_SWINGING_STRIKE_SAFE_PASSED_BALL = auto()  # []
    PITCHER_SWINGING_STRIKE_SAFE_WILD_PITCH = auto()  # []
    PITCHER_WILD_PITCH = auto()  # []

    RUNNER_STEAL_SECOND_OUT = auto()  # [player]
    RUNNER_STEAL_SECOND_SAFE = auto()  # [player]
    RUNNER_STEAL_SECOND_THROWING_ERROR = auto()  # [player]
    RUNNER_TO_SECOND_NO_THROW = auto()  # [player]

    RUNNER_STEAL_THIRD_OUT = auto()  # [player]
    RUNNER_STEAL_THIRD_SAFE = auto()  # [player]
    RUNNER_TO_THIRD_NO_THROW = auto()  # [player]

    RUNNER_SCORES_NO_THROW = auto()  # [player]

    RUNNER_ON_FIRST_TO_SECOND_NO_THROW = auto()  # []

    RUNNER_ON_SECOND_TO_THIRD_NO_THROW = auto()  # []
    RUNNER_ON_SECOND_TO_THIRD_THROW_MADE = auto()  # []
    RUNNER_ON_SECOND_OUT_AT_THIRD_THROW_MADE = auto()  # []

    RUNNER_ON_THIRD_SCORES_NO_THROW = auto()  # []
    RUNNER_ON_THIRD_SCORES_THROW_MADE = auto()  # []
    RUNNER_ON_THIRD_OUT_AT_HOME_THROW_MADE = auto()  # []
    RUNNER_ON_THIRD_SCORES_OUT_AT_THIRD = auto()  # []
    RUNNER_ON_THIRD_SCORES_SAFE_AT_THIRD = auto()  # []

    NONE = auto()  # []
