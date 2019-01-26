#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data (non-reloadable) object for a serializable enum."""

import logging
from enum import IntEnum

_logger = logging.getLogger('filefairy')


class Enum(IntEnum):
    @classmethod
    def decode(cls, encoding):
        try:
            member, args = encoding.split(' ', 1)
            return (cls[member.upper()], [a.strip() for a in args.split()])
        except Exception as e:
            _logger.log(logging.WARNING, 'Handled warning.', exc_info=True)
            return (None, [])

    def encode(self, *args):
        return ' '.join([self.name.lower()] + list(args))
