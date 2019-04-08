#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for math operations."""


def crange(start, end, modulo):
    """Simulate a circular range generator.

    Args:
        start: The start of the range.
        end: The end of the range.
        modulo: The upper bound of the range.

    Yields:
        The circular range.
    """
    if start > end:
        while start < modulo:
            yield start
            start += 1
        start = 0

    while start <= end:
        yield start
        start += 1
