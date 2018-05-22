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

    @staticmethod
    def check_args_value(value):
        if not isinstance(value, tuple):
            raise ValueError(value)

    @staticmethod
    def check_kwargs_value(value):
        if not isinstance(value, dict):
            raise ValueError(value)

    def get_target(self):
        return self._target

    def set_target(self, value):
        self.check_target_value(value)
        self._target = value

    def get_args(self):
        return self._args

    def set_args(self, value):
        if value is None:
            self._args = tuple()
        else:
            self.check_args_value(value)
            self._args = value

    def get_kwargs(self):
        return self._kwargs

    def set_kwargs(self, value):
        if value is None:
            self._kwargs = dict()
        else:
            self.check_kwargs_value(value)
            self._kwargs = value

    target = property(get_target, set_target)
    args = property(get_args, set_args)
    kwargs = property(get_kwargs, set_kwargs)

    def execute(self):
        self.target(*self.args, **self.kwargs)
