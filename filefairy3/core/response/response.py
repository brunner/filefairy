#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/core/response', '', _path))
from core.notify.notify import Notify  # noqa
from core.task.task import Task  # noqa


class Response(object):
    def __init__(self, notify=None, shadow=None, task=None):
        self.notify = notify
        self.shadow = shadow
        self.task = task

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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
    def check_shadow_dict(values):
        if not isinstance(values, dict):
            raise TypeError(values)
        for key in values.keys():
            Response.check_shadow_key(key)
        for value in values.values():
            Response.check_shadow_value(value)

    @staticmethod
    def check_shadow_key(key):
        if not isinstance(key, str):
            raise ValueError(key)

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

    @staticmethod
    def check_shadow_value(value):
        if not isinstance(value, dict):
            raise ValueError(value)

    def get_notify(self):
        return self._notify

    def get_shadow(self):
        return self._shadow

    def get_task(self):
        return self._task

    def set_notify(self, values):
        if values is None:
            self._notify = []
        else:
            self.check_notify_list(values)
            self._notify = values

    def set_shadow(self, values):
        if values is None:
            self._shadow = {}
        else:
            self.check_shadow_dict(values)
            self._shadow = values

    def set_task(self, values):
        if values is None:
            self._task = []
        else:
            self.check_task_list(values)
            self._task = values

    notify = property(get_notify, set_notify)
    shadow = property(get_shadow, set_shadow)
    task = property(get_task, set_task)

    def append_notify(self, value):
        self.check_notify_value(value)
        self._notify.append(value)

    def append_task(self, value):
        self.check_task_value(value)
        self._task.append(value)
