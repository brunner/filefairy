#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for regular expressions."""

import re


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
        return [[g.strip() for g in m] for m in match]

    return [m.strip() for m in match]


def find(pattern, string):
    """Convenience wrapper around re.findall which returns the first match.

    Returns the first match of pattern in string, or None if no match is found.
    The returned match is a single string (or None) if pattern has a single
    group, or a list of strings (or None) if pattern has multiple groups.

    Args:
        pattern: The regular expression pattern to match.
        string: The string to scan for the pattern.

    Returns:
        The matched group(s) of pattern within string.
    """
    match = findall(pattern, string)
    if match:
        return match[0]

    groups = re.compile(pattern).groups
    if groups > 1:
        return [None] * groups

    return None
