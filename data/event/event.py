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
    """Describe a number of different types of events that happen in a game."""

    """The player batting has changed.

    Attributes:
        encoding: The encoding identifying the new batter.
    """
    CHANGE_BATTER = 1

    """The player pitching has changed.

    Attributes:
        encoding: The encoding identifying the new pitcher.
    """
    CHANGE_PITCHER = 2
