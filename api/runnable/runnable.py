#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the runnable API to set up hooks for standard task interactions.

This base class describes the following interactions that the app expects to
perform on a running task.

    * Notify: Receive signals indicating global state from the app.
    * Run: Perform some repeating (about once per minute) functionality.
    * Setup: Execute some code during task initialization.
    * Shadow: Store some information which was calculated by a different task.

The base class also has properties for ``date``, used to timestamp the most
recent usage of the task, and ``ok``, used to represent whether the task is
actively running or has experienced failure.

Instances of runnable are required to return Response data from
_notify_internal, _run_internal, and _setup_internal.
"""

import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/runnable', '', _path))

from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa


class Runnable():
    def __init__(self, **kwargs):
        date = kwargs.pop('date')
        super(Runnable, self).__init__(**kwargs)

        self.date = date
        self.ok = True

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def check_date_value(value):
        if not isinstance(value, datetime.datetime):
            raise ValueError(value)

    @staticmethod
    def check_ok_value(value):
        if not isinstance(value, bool):
            raise ValueError(value)

    def get_date(self):
        return self._date

    def get_ok(self):
        return self._ok

    def set_date(self, value):
        self.check_date_value(value)
        self._date = value

    def set_ok(self, value):
        self.check_ok_value(value)
        self._ok = value

    date = property(get_date, set_date)
    ok = property(get_ok, set_ok)

    def _notify_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        return Response()

    def _notify(self, **kwargs):
        response = self._notify_internal(**kwargs)
        if response.notify:
            response.notify = [Notify.BASE]
        return response

    def _run(self, **kwargs):
        return self._run_internal(**kwargs)

    def _setup(self, **kwargs):
        return self._setup_internal(**kwargs)
