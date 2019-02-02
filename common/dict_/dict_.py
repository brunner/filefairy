#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for dictionary manipulations."""


def merge(d1, d2, f, empty):
    """Merge two dictionaries, given a merge function.

    The merged dictionary contains all keys from the two dictionaries, with the
    merged value for each key being the result of applying the merge function
    to the original values. If a key is not present in either dictionary, then
    the provided empty value is used instead.

    Args:
        d1: The first dictionary.
        d2: The second dictionary.
        f: The merge function.
        empty: The value to use in case a key is not present in a dictionary.

    Returns:
        The merged dictionary.
    """
    keys = set(d1).union(d2)
    return {k: f(d1.get(k, empty), d2.get(k, empty)) for k in keys}
