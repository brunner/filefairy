#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/value/task', '', _path))


class Task(object):
    def __init__(self, target=None, args=None, kwargs=None):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def check_target_value(value):
        if not callable(value):
            raise ValueError(value)

    def get_target(self):
        return self._target

    def set_target(self, value):
        self.check_target_value(value)
        self._target = value

    target = property(get_target, set_target)

    def execute(self):
        self.target(*self.args, **self.kwargs)
