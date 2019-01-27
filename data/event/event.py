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
    HIT_SINGLE = auto()  # [path, zone]
    HIT_DOUBLE = auto()  # [path, zone]
    HIT_HOME_RUN = auto()  # [zone, distance]
    OUT_FLY_OUT = auto()  # [scoring, path, zone]
    OUT_GROUND_OUT = auto()  # [scoring, zone]
    PITCH_BALL = auto()  # []
    PITCH_CALLED_STRIKE = auto()  # []
    PITCH_FOULED_STRIKE = auto()  # []
    PITCH_SWINGING_STRIKE = auto()  # []
    RUNNER_STEALS_SECOND = auto()  # [player]
    RUNNER_OUT_STEALING_SECOND = auto()  # [player]
    RUNNER_TO_SECOND = auto()  # [player]
    RUNNER_STEALS_THIRD = auto()  # [player]
    RUNNER_OUT_STEALING_THIRD = auto()  # [player]
    RUNNER_TO_THIRD = auto()  # [player]
    RUNNER_SCORES_NO_THROW = auto()  # [player]
    RUNNER_ON_FIRST_PICKED_OFF = auto()  # []
    RUNNER_ON_THIRD_SCORES_NO_THROW = auto()  # []
    RUNNER_ON_THIRD_SCORES_THROW_MADE = auto()  # []
    SAC_BUNT_OUT_AT_SECOND = auto()  # [scoring]
