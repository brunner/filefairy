#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the nameable API to describe a task's name.

Example:
    class Task(Nameable):
        def __init__(self, **kwargs):
            super(Task, self).__init__(**kwargs)

        def _name(self):
            return 'Task'
"""

import abc
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/nameable', '', _path))

from common.abc_.abc_ import abstractstatic  # noqa


class Nameable():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abc.abstractmethod
    def _name(self):
        pass
