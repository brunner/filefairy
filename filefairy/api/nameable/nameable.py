#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/nameable', '', _path))

from util.abc_.abc_ import abstractstatic  # noqa


class Nameable(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(Nameable, self).__init__()

    @abstractstatic
    def _info():
        pass

    @abc.abstractmethod
    def _name(self):
        pass
