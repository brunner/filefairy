#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for regular expressions."""

import re


def find(pattern, string, flags=0):
    """Convenience wrapper around re.findall.

    Returns the first match of pattern in string, or None if no match is found.
    The returned match is a single string (or None) if pattern has a single
    group, or a list of strings (or None) if pattern has multiple groups.

    Args:
        pattern: The regular expression pattern to match.
        string: The string to scan for the pattern.

    Returns:
        The matched group(s) of pattern within string.
    """
    groups = re.compile(pattern).groups
    match = re.findall(pattern, string)

    if groups > 1:
        return [m.strip() for m in match[0]] if match else [None] * groups

    return match[0].strip() if match else None
