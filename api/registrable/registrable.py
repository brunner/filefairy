#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the registrable API to set up hooks for standard task interactions.

This base class collects the functionality of several sub-APIs to describe the
following interactions that the app expects to perform on a running task.

    * Notify: Receive signals indicating global state from the app.
    * Run: Perform some repeating (about once per minute) functionality.
    * Setup: Execute some code during task initialization.
    * Shadow: Store some information which was calculated by a different task.

The base class also has properties for ``date``, used to timestamp the most
recent usage of the task, and ``ok``, used to represent whether the task is
actively running or has experienced failure.

Instances of registrable are required to return Response data from
_notify_internal, _run_internal, and _setup_internal, and Shadow data from
_shadow_internal.
"""

import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/registrable', '', _path))

from api.messageable.messageable import Messageable  # noqa
from api.reloadable.reloadable import Reloadable  # noqa
from api.renderable.renderable import Renderable  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa


class Registrable(Messageable, Reloadable, Renderable):
    def __init__(self, **kwargs):
        date = kwargs.pop('date')
        super().__init__(**kwargs)

        self.date = date
        self.ok = True
        self.shadow = {}

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

    def _shadow_data(self, **kwargs):
        return []

    def _notify_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        return Response()

    def _shadow_internal(self, **kwargs):
        return Response()

    def _notify(self, **kwargs):
        response = self._notify_internal(**kwargs)
        if response.notify:
            response.notify = [Notify.BASE]
        return response

    def _run(self, **kwargs):
        return self._run_internal(**kwargs)

    def _setup(self, **kwargs):
        self._reload(**kwargs)
        response = self._setup_internal(**kwargs)
        response.shadow = self._shadow_data()
        self._render(**kwargs)
        return response

    def _shadow(self, **kwargs):
        shadow = kwargs['shadow']
        self.shadow[shadow.key] = shadow.info
        return self._shadow_internal(**kwargs)
