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
        distance: A batted ball's travel distance. For example, `402`.
        path: A batted ball's flight path. For example, `F` for a fly ball.
        player: A player that the event describes. For example, `P24322`.
        scoring: A scoring notation for the event. For example, `4-3`.
        zone: A batted ball's location. For example, `7LD`.
    """

    CHANGE_BATTER = auto()  # [player]
    CHANGE_INNING = auto()  # []
    CHANGE_PITCHER = auto()  # [player]

    BATTER_INFIELD_SINGLE = auto()  # [path, zone]
    BATTER_SINGLE = auto()  # [path, zone]
    BATTER_DOUBLE = auto()  # [path, zone]
    BATTER_HOME_RUN = auto()  # [zone, distance]

    BATTER_FLY_OUT = auto()  # [scoring, path, zone]
    BATTER_GROUND_OUT = auto()  # [scoring, zone]
    BATTER_GROUNDS_INTO_DOUBLE_PLAY = auto()  # [scoring, zone]
    BATTER_SAC_BUNT_OUT_AT_SECOND = auto()  # [scoring]

    PITCHER_BALL = auto()  # []
    PITCHER_CALLED_STRIKE = auto()  # []
    PITCHER_FOULED_STRIKE = auto()  # []
    PITCHER_FOULED_STRIKE_WITH_ERROR = auto()  # [scoring]
    PITCHER_SWINGING_STRIKE = auto()  # []
    PITCHER_WILD_PITCH = auto()  # []

    RUNNER_STEAL_SECOND_SAFE = auto()  # [player]
    RUNNER_STEAL_SECOND_OUT = auto()  # [player]
    RUNNER_TO_SECOND_NO_THROW = auto()  # [player]

    RUNNER_STEAL_THIRD_SAFE = auto()  # [player]
    RUNNER_STEAL_THIRD_OUT = auto()  # [player]
    RUNNER_TO_THIRD_NO_THROW = auto()  # [player]

    RUNNER_SCORES_NO_THROW = auto()  # [player]

    RUNNER_ON_FIRST_PICKED_OFF = auto()  # []

    RUNNER_ON_SECOND_TO_THIRD_THROW_MADE = auto()  # []

    RUNNER_ON_THIRD_SCORES_NO_THROW = auto()  # []
    RUNNER_ON_THIRD_SCORES_THROW_MADE = auto()  # []
    RUNNER_ON_THIRD_OUT_AT_HOME_THROW_MADE = auto()  # []
