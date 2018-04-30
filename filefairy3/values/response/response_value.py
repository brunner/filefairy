#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/values/response', '', _path))
from values.notify.notify_value import NotifyValue  # noqa


class ResponseValue(object):
    def __init__(self, notify=None, shadow=None):
        self.notify = notify
        self.shadow = shadow

    @staticmethod
    def check_notify(value):
        if not isinstance(value, list):
            raise TypeError(value)
        if any(not isinstance(v, NotifyValue) for v in value):
            raise ValueError(value)
        return value

    @staticmethod
    def check_shadow(value):
        if not isinstance(value, dict):
            raise TypeError(value)
        if any(not isinstance(k, str) for k in value.keys()):
            raise ValueError(value)
        if any(not isinstance(v, dict) for v in value.values()):
            raise ValueError(value)
        return value

    def get_notify(self):
        return self._notify

    def get_shadow(self):
        return self._shadow

    def set_notify(self, value):
        if value is None:
            self._notify = []
        else:
            self._notify = self.check_notify(value)

    def set_shadow(self, value):
        if value is None:
            self._shadow = {}
        else:
            self._shadow = self.check_shadow(value)

    notify = property(get_notify, set_notify)
    shadow = property(get_shadow, set_shadow)
