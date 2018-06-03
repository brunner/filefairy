#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import datetime


class Registrable():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        date = kwargs.pop('date')
        super().__init__(**kwargs)

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
