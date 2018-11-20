#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy


class Debug(object):
    def __init__(self, msg=None, extra=None):
        self.msg = msg
        self.extra = extra

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def check_msg_value(value):
        if not isinstance(value, str):
            raise ValueError(value)

    @staticmethod
    def check_extra_value(value):
        if not isinstance(value, dict):
            raise ValueError(value)

    def get_msg(self):
        return self._msg

    def set_msg(self, value):
        self.check_msg_value(value)
        self._msg = value

    def get_extra(self):
        return self._extra

    def set_extra(self, value):
        if value is None:
            self._extra = {}
        else:
            self.check_extra_value(value)
            self._extra = copy.deepcopy(value)

    msg = property(get_msg, set_msg)
    extra = property(get_extra, set_extra)
