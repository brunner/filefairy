#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for math operations."""


def crange(start, modulo):
    """Simulate a circular range generator.

    Args:
        start: The start (and end) of the range.
        modulo: The upper bound of the range.

    Yields:
        The circular range.
    """
    i = start
    while i < modulo:
        yield i
        i += 1
    i = 0
    while i < start:
        yield i
        i += 1
