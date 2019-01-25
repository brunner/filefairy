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
            return cls[encoding.upper()]
        except Exception as e:
            _logger.log(logging.WARNING, 'Handled warning.', exc_info=True)
            return None

    @property
    def encoding(self):
        return self.name.lower()
