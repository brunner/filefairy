#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/values/response', '', _path))
from values.notification.notification_value import NotificationValue  # noqa


class ResponseValue(object):
    def __init__(self, notification=None, shadow=None):
        self.notification = notification
        self.shadow = shadow

    @staticmethod
    def check_notification(value):
        if not isinstance(value, list):
            raise TypeError(value)
        if any(not isinstance(v, NotificationValue) for v in value):
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

    def get_notification(self):
        return self._notification

    def get_shadow(self):
        return self._shadow

    def set_notification(self, value):
        if value is None:
            self._notification = []
        else:
            self._notification = self.check_notification(value)

    def set_shadow(self, value):
        if value is None:
            self._shadow = {}
        else:
            self._shadow = self.check_shadow(value)

    notification = property(get_notification, set_notification)
    shadow = property(get_shadow, set_shadow)
