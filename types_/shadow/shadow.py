#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data (non-reloadable) object for sharing information between tasks."""

import copy


class Shadow(object):
    """Describe a piece of information that one task shares with another."""
    def __init__(self, destination=None, key=None, info=None):
        """Create a Shadow object.

        Args:
            destination: The task to share the information with.
            key: The key the destination should use to index the information.
            info: The information to share.
        """
        self.destination = destination
        self.key = key
        self.info = info

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def check_destination_value(value):
        if not isinstance(value, str):
            raise ValueError(value)

    @staticmethod
    def check_key_value(value):
        if not isinstance(value, str):
            raise ValueError(value)

    def get_destination(self):
        return self._destination

    def set_destination(self, value):
        self.check_destination_value(value)
        self._destination = value

    def get_key(self):
        return self._key

    def set_key(self, value):
        self.check_key_value(value)
        self._key = value

    def get_info(self):
        return self._info

    def set_info(self, value):
        self._info = copy.deepcopy(value)

    destination = property(get_destination, set_destination)
    key = property(get_key, set_key)
    info = property(get_info, set_info)
