#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for gameday.py."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/gameday', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa
from tasks.gameday.gameday import Gameday  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)


class GamedayTest(Test):
    def init_mocks(self, data):
        pass


if __name__ in ['__main__', 'tasks.gameday.gameday_test']:
    main(
        GamedayTest,
        Gameday,
        'tasks.gameday',
        'tasks/gameday', {},
        __name__ == '__main__',
        date=DATE_10260602,
        e=ENV)
