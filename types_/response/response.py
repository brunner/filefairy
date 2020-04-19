#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data (non-reloadable) object for grouping task return values."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/types_/response', '', _path))
from types_.debug.debug import Debug  # noqa
from types_.notify.notify import Notify  # noqa
from types_.thread_.thread_ import Thread  # noqa


class Response(object):
    """Describe a group of data types that a task might return to the app."""
    def __init__(self, debug=None, notify=None, thread_=None):
        """Create a Response object.

        Args:
            debug: The optional Debug object(s) in the response.
            notify: The optional Notify object(s) in the response.
            thread_: The optional Thread object(s) in the response.
        """
        self.debug = debug
        self.notify = notify
        self.thread_ = thread_

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
    def check_thread_list(values):
        if not isinstance(values, list):
            raise TypeError(values)
        for value in values:
            Response.check_thread_value(value)

    @staticmethod
    def check_thread_value(value):
        if not isinstance(value, Thread):
            raise ValueError(value)

    def get_debug(self):
        return self._debug

    def get_notify(self):
        return self._notify

    def get_thread(self):
        return self._thread_

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

    def set_thread(self, values):
        if values is None:
            self._thread_ = []
        else:
            self.check_thread_list(values)
            self._thread_ = values

    debug = property(get_debug, set_debug)
    notify = property(get_notify, set_notify)
    thread_ = property(get_thread, set_thread)

    def append(self, debug=None, notify=None, thread_=None):
        """Append additional data to a Response object.

        Args:
            debug: The optional Debug object to append.
            notify: The optional Notify object to append.
            thread_: The optional Thread object to append.
        """
        if debug:
            self.check_debug_value(debug)
            self._debug.append(debug)

        if notify:
            self.check_notify_value(notify)
            self._notify.append(notify)

        if thread_:
            self.check_thread_value(thread_)
            self._thread_.append(thread_)
