#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for regular expressions."""

import re


def _strip(s):
    if s is None:
        return None
    return s.strip()


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


def find(pattern, string, force_groups=False):
    """Convenience wrapper around re.search which returns the first match.

    Returns the first match of pattern in string, or None if no match is found.
    The returned match is a single string (or None) if pattern has a single
    group, or a list of strings (or None) if pattern has multiple groups.

    If force_groups=True and the pattern has no groups, return an empty list
    instead of the entire matched pattern.

    Args:
        pattern: The regular expression pattern to match.
        string: The string to scan for the pattern.
        force_groups: Whether to restrict the returned matches to groups only.

    Returns:
        The matched group(s) of pattern within string.
    """
    groups = re.compile(pattern).groups
    match = re.search(pattern, string)

    if not match:
        return [None] * groups if groups > 1 and not force_groups else None

    if groups > 1:
        try:
            return [_strip(g) for g in match.groups()]
        except:
            print(pattern, string, match.groups())
            raise

    if groups == 0 and force_groups:
        return []

    m = _strip(match[groups])
    return [m] if force_groups else m
