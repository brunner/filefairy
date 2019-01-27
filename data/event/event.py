#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data (non-reloadable) object for game event codes."""

import os
import re
import sys

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

    CHANGE_BATTER = 1  # [player]
    CHANGE_INNING = 2  # []
    CHANGE_PITCHER = 3  # [player]
    HIT_SINGLE = 4  # [path, zone]
    HIT_DOUBLE = 5  # [path, zone]
    HIT_HOME_RUN = 6  # [zone, distance]
    OUT_FLY_OUT = 7  # [scoring, path, zone]
    OUT_GROUND_OUT = 8  # [scoring, zone]
    PITCH_BALL = 9  # []
    PITCH_CALLED_STRIKE = 10  # []
    PITCH_FOULED_STRIKE = 11  # []
    PITCH_SWINGING_STRIKE = 12  # []
    RUNNER_STEALS_SECOND = 13  # [player]
    RUNNER_OUT_STEALING_SECOND = 14  # [player]
    RUNNER_TO_SECOND = 15  # [player]
    RUNNER_STEALS_THIRD = 16  # [player]
    RUNNER_OUT_STEALING_THIRD = 17  # [player]
    RUNNER_TO_THIRD = 18  # [player]
    RUNNER_SCORES_NO_THROW = 19  # [player]
    RUNNER_ON_FIRST_PICKED_OFF = 20  # []
    RUNNER_ON_THIRD_SCORES_NO_THROW = 21  # []
    RUNNER_ON_THIRD_SCORES_THROW_MADE = 22  # []
    SAC_BUNT_OUT_AT_SECOND = 23  # [scoring]
