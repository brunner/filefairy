#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for JSON operations."""

import json
import logging

_logger = logging.getLogger('filefairy')


class Encoder(json.JSONEncoder):
    """Encoder guarding against accidental failures if storing complex data."""

    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception:
            _logger.log(logging.WARNING, 'Handled warning.', exc_info=True)
            return ''


def dumps(data):
    """Convenience wrapper around json.dumps.

    Sorts, indents, and uses safe encoder when dumping arbitrary data.

    Args:
        data: Dictionary to dump as safe, pretty-printed JSON string.

    Returns:
        The JSON string.
    """
    return json.dumps(data, indent=2, sort_keys=True, cls=Encoder)
