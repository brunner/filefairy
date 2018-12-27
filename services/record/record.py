#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for describing and displaying team records."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/record', '', _path))


def decode_record(string):
    """Parses an encoded W-L record string into a tuple of wins and losses.

    Args:
        s: The encoded record string.

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
