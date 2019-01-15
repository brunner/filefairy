#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for serializing team records."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/record', '', _path))


def add_records(string1, string2):
    """Adds two encoded W-L record strings.

    Args:
        string1: The first encoded record string.
        string2: The second encoded record string.

    Returns:
        A string representation for the resulting record.
    """
    w1, l1 = decode_record(string1)
    w2, l2 = decode_record(string2)
    return encode_record(w1 + w2, l1 + l2)


def decode_record(string):
    """Parses an encoded W-L record string into a tuple of wins and losses.

    Args:
        string: The encoded record string.

    Returns:
        A tuple of wins and losses.
    """
    return tuple(int(x) for x in string.split('-'))


def encode_record(w, l):
    """Encodes a set of integer W-L values into a record string.

    Args:
        w: The wins.
        l: The losses.

    Returns:
        A string representation for the given record.
    """
    return '{}-{}'.format(w, l)
