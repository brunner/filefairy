#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/core/response', '', _path))
from core.debug.debug import Debug  # noqa
from core.notify.notify import Notify  # noqa
from core.shadow.shadow import Shadow  # noqa
from core.task.task import Task  # noqa


class Response(object):
    def __init__(self, debug=None, notify=None, shadow=None, task=None):
        self.debug = debug
        self.notify = notify
        self.shadow = shadow
        self.task = task

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def check_debug_list(values):
        if not isinstance(values, list):
            raise TypeError(values)
        for value in values:
            Response.check_debug_value(value)

    @staticmethod
    def check_debug_value(value):
        if not isinstance(value, Debug):
            raise ValueError(value)

    @staticmethod
    def check_notify_list(values):
        if not isinstance(values, list):
            raise TypeError(values)
        for value in values:
            Response.check_notify_value(value)

    @staticmethod
    def check_notify_value(value):
        if not isinstance(value, Notify):
            raise ValueError(value)

    @staticmethod
    def check_shadow_list(values):
        if not isinstance(values, list):
            raise TypeError(values)
        for value in values:
            Response.check_shadow_value(value)

    @staticmethod
    def check_shadow_value(value):
        if not isinstance(value, Shadow):
            raise ValueError(value)

    @staticmethod
    def check_task_list(values):
        if not isinstance(values, list):
            raise TypeError(values)
        for value in values:
            Response.check_task_value(value)

    @staticmethod
    def check_task_value(value):
        if not isinstance(value, Task):
            raise ValueError(value)

    def get_debug(self):
        return self._debug

    def get_notify(self):
        return self._notify

    def get_shadow(self):
        return self._shadow

    def get_task(self):
        return self._task

    def set_debug(self, values):
        if values is None:
            self._debug = []
        else:
            self.check_debug_list(values)
            self._debug = values

    def set_notify(self, values):
        if values is None:
            self._notify = []
        else:
            self.check_notify_list(values)
            self._notify = values

    def set_shadow(self, values):
        if values is None:
            self._shadow = []
        else:
            self.check_shadow_list(values)
            self._shadow = values

    def set_task(self, values):
        if values is None:
            self._task = []
        else:
            self.check_task_list(values)
            self._task = values

    debug = property(get_debug, set_debug)
    notify = property(get_notify, set_notify)
    shadow = property(get_shadow, set_shadow)
    task = property(get_task, set_task)

    def append_debug(self, value):
        self.check_debug_value(value)
        self._debug.append(value)

    def append_notify(self, value):
        self.check_notify_value(value)
        self._notify.append(value)

    def append_shadow(self, value):
        self.check_shadow_value(value)
        self._shadow.append(value)

    def append_task(self, value):
        self.check_task_value(value)
        self._task.append(value)
