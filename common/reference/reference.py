#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for safely using the reference."""

import os
import re
import sys
from functools import partial

_path = os.path.dirname(os.path.abspath(__file__))
_reference = None
sys.path.append(re.sub(r'/tasks/news', '', _path))

from common.elements.elements import anchor  # noqa

SEPARATORS = [' de ', ' De ', ' La ', ' Montes ', ' van ', ' Vander ', ' ']


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


def player_to_link(e):
    """Gets the player's link.

    Args:
        e: The player's encoding.

    Returns:
        The player's link.
    """
    url = 'https://statsplus.net/oblootp/player/' + e.lstrip('P')
    return anchor(url, _get(e, 4, 'Jim Unknown'))


def player_to_link_sub(text):
    """Substitutes all player encodings with the corresponding links.

    Args:
        text: The text to replace.

    Returns:
        The substituted text.
    """
    return _sub(partial(_repl, player_to_link), text)


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


def player_to_shortname(e):
    """Gets the player's short name.

    Args:
        e: The player's encoding.

    Returns:
        The player's short name.
    """
    name = player_to_name(e)
    for s in SEPARATORS:
        if s in name:
            first, last = name.rsplit(s, 1)
            return first[0] + '.' + s + last
    return name


def player_to_shortname_sub(text):
    """Substitutes all player encodings with the corresponding short name.

    Args:
        text: The text to replace.

    Returns:
        The substituted text.
    """
    return _sub(partial(_repl, player_to_shortname), text)


def player_to_starter(e):
    """Gets the player's starter text.

    Args:
        e: The player's encoding.

    Returns:
        The player's starter text.
    """
    throws = player_to_throws(e)
    name = player_to_name(e)
    return name + ' (' + throws + ')'


def player_to_starter_sub(text):
    """Substitutes all player encodings with the corresponding starter text.

    Args:
        text: The text to replace.

    Returns:
        The substituted text.
    """
    return _sub(partial(_repl, player_to_starter), text)


def player_to_team(e):
    """Gets the player's team.

    Args:
        e: The player's encoding.

    Returns:
        The player's team.
    """
    return _get(e, 0, 'T30')


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
