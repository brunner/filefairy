#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for safely using the reference."""

from functools import partial

_reference = None


def _get(num, index, default):
    if _reference is None:
        return default
    return _reference._get(num, index, default)


def _put(players):
    if _reference is not None:
        _reference._put(players)


def _repl(f, m):
    return f(m.group(0).strip('P'))


def _sub(repl, text):
    if _reference is None:
        return text
    return _reference._sub(repl, text)


def set_reference(reference):
    """Sets the reference object.

    Args:
        reference: The reference object.
    """
    global _reference
    _reference = reference


def player_to_bats(num):
    """Gets the player's batting handedness (``L``, ``R``, or ``S``).

    Args:
        num: The player's id number.

    Returns:
        The player's batting handedness.
    """
    return _get(num, 2, 'R')


def player_to_name(num):
    """Gets the player's full name.

    Args:
        num: The player's id number.

    Returns:
        The player's full name.
    """
    return _get(num, 4, 'Jim Unknown')


def player_to_name_sub(text):
    """Substitutes all player id numbers with the corresponding full name.

    Args:
        text: The text to replace.

    Returns:
        The substituted text.
    """
    return _sub(partial(_repl, player_to_name), text)


def player_to_number(num):
    """Gets the player's jersey number.

    Args:
        num: The player's id number.

    Returns:
        The player's jersey number.
    """
    return _get(num, 1, '0')


def player_to_team(num):
    """Gets the player's team.

    Args:
        num: The player's id number.

    Returns:
        The player's team.
    """
    return _get(num, 0, 'T??')


def player_to_throws(num):
    """Gets the player's throwing handedness (``L`` or ``R``).

    Args:
        num: The player's id number.

    Returns:
        The player's throwing handedness.
    """
    return _get(num, 3, 'R')
