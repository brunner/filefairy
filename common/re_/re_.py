#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for regular expressions."""

import re


def _strip(s):
    if s is None:
        return None
    return s.strip()


def _transform(pattern, match, group):
    groups = re.compile(pattern).groups

    if not match:
        return [None] * groups if groups > 1 and not group else None

    if groups > 1:
        return [_strip(g) for g in match.groups()]

    if groups == 1:
        m = _strip(match.groups()[0])
        return [m] if group else m

    return [] if group else match.group()


def findall(pattern, string):
    """Convenience wrapper around re.findall which returns all matches.

    Returns all matches of pattern in string, or an empty list if no match is
    found. The matches are a single string (or None) if pattern has a single
    group, or a list of strings (or None) if pattern has multiple groups.

    Args:
        pattern: The regular expression pattern to match.
        string: The string to scan for the pattern.

    Returns:
        The list of matched group(s) of pattern within string.
    """
    groups = re.compile(pattern).groups
    match = re.findall(pattern, string)

    if groups > 1:
        return [[_strip(g) for g in m] for m in match]

    return [_strip(m) for m in match]


def match(pattern, string):
    """Convenience wrapper around re.match.

    Returns the first match of pattern at the beginning of string, or None if
    no match is found. The returned match is a list of strings if pattern has
    at least one pattern group, or an empty list if pattern has no groups.

    Args:
        pattern: The regular expression pattern to match.
        string: The string to scan for the pattern.

    Returns:
        The re.match matches of pattern within string.
    """
    return _transform(pattern, re.match(pattern, string), True)


def search(pattern, string):
    """Convenience wrapper around re.search.

    Returns the first match of pattern anywhere in string, or None if no match
    is found. If found, the returned match is a single string if pattern has a
    single pattern group, or a list of strings if pattern has multiple groups.

    Args:
        pattern: The regular expression pattern to match.
        string: The string to scan for the pattern.

    Returns:
        The re.search matches of pattern within string.
    """
    return _transform(pattern, re.search(pattern, string), False)
