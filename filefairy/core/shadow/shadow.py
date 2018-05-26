#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy


class Shadow(object):
    def __init__(self, destination=None, key=None, data=None):
        self.destination = destination
        self.key = key
        self.data = data

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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

    def get_data(self):
        return self._data

    def set_data(self, value):
        self._data = copy.deepcopy(value)

    destination = property(get_destination, set_destination)
    key = property(get_key, set_key)
    data = property(get_data, set_data)
