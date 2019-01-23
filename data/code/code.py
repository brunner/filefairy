#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data (non-reloadable) object for play identification."""

from enum import IntEnum


class Code(IntEnum):
    """Describe a number of different types of plays that happen in a game."""

    """The player batting has changed.

    Attributes:
        encoding: The encoding identifying the new batter.
    """
    BATTER = 1

    """The player pitching has changed.

    Attributes:
        encoding: The encoding identifying the new pitcher.
    """
    PITCHER = 2
