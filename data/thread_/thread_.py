#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data (non-reloadable) object for threaded functions."""


class Thread(object):
    """Describe a function to be run in a thread in the app background."""

    def __init__(self, target=None, args=None, kwargs=None):
        """Create a Thread object.

        Args:
            target: The function name.
            args: The optional positional argument(s) to pass to the function.
            kwargs: The optional keyword argument(s) to pass to the function.
        """
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def check_target_value(value):
        if not isinstance(value, str):
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
