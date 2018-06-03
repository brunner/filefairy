#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/registrable', '', _path))
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa


class Registrable():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        date = kwargs.pop('date')
        super().__init__(**kwargs)

        self.date = date
        self.ok = True
        self.shadow = {}

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @abc.abstractproperty
    def enabled(self):
        pass

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

    @abc.abstractmethod
    def _notify_internal(self, **kwargs):
        pass

    @abc.abstractmethod
    def _setup_internal(self, **kwargs):
        pass

    @abc.abstractmethod
    def _shadow_internal(self, **kwargs):
        pass

    def _notify(self, **kwargs):
        response = self._notify_internal(**kwargs)
        if response.notify:
            response.notify = [Notify.BASE]
        return response

    def _setup(self, **kwargs):
        response = self._setup_internal(**kwargs)
        response.shadow = self._shadow_internal(**kwargs)
        return response

    def _shadow(self, **kwargs):
        shadow = kwargs['shadow']
        self.shadow[shadow.key] = shadow.data
        self._setup(**kwargs)
        return Response()
