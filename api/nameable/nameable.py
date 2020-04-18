#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the nameable API to describe a task's name.

Example:
    class Task(Nameable):
        def __init__(self, **kwargs):
            super(Task, self).__init__(**kwargs)
"""

import abc


class Nameable():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _name(self):
        return self.__class__.__name__.lower()
