#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for safely using the reference."""

from functools import partial

_reference = None


def _get(num, index, default):
    if _reference is None:
        return default
    return _reference._get(num, index, default)


def _repl(f, m):
    return f(m.group(0))


def _sub(repl, text):
    if _reference is None:
        return text
    return _reference._sub(repl, text)


def player_to_bats(e):
    """Gets the player's batting handedness (``L``, ``R``, or ``S``).

    Args:
        e: The player's encoding.

    Returns:
        The player's batting handedness.
    """
    return _get(e, 2, 'R')


def player_to_name(e):
    """Gets the player's full name.

    Args:
        e: The player's encoding.

    Returns:
        The player's full name.
    """
    return _get(e, 4, 'Jim Unknown')


def player_to_name_sub(text):
    """Substitutes all player encodings with the corresponding full name.

    Args:
        text: The text to replace.

    Returns:
        The substituted text.
    """
    return _sub(partial(_repl, player_to_name), text)


def player_to_number(e):
    """Gets the player's jersey number.

    Args:
        e: The player's encoding.

    Returns:
        The player's jersey number.
    """
    return _get(e, 1, '0')


def player_to_team(e):
    """Gets the player's team.

    Args:
        e: The player's encoding.

    Returns:
        The player's team.
    """
    return _get(e, 0, 'T??')


def player_to_throws(e):
    """Gets the player's throwing handedness (``L`` or ``R``).

    Args:
        e: The player's encoding.

    Returns:
        The player's throwing handedness.
    """
    return _get(e, 3, 'R')


def put_players(players):
    if _reference is not None:
        _reference._put(players)


def set_reference(reference):
    """Sets the reference object.

    Args:
        reference: The reference object.
    """
    global _reference
    _reference = reference
