#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for storing gameday player information."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/tables', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import tbody  # noqa


class Tables(object):
    def __init__(self):
        self.live_summaries = []
        self.live_pitch = table()
        self.live_pitches = []
        self.live_play = table()
        self.live_play = []
        self.live_tables = []

        self.old_body = []
        self.old_table = table()
        self.old_tables = []
        self.summary = []

    def append_live_table(self, t):
        self.live_tables.append(t)

    def append_all(self):
        for row in self.old_body:
            tbody(self.old_table, row)

    def append_old_body(self, row):
        self.old_body.append(row)

    def append_summary(self, s):
        self.summary.append(s)

    def create_old_table(self, roster, state):
        bcols = [col(), col(clazz='w-50p text-right')]
        body, self.old_body = list(self.old_body), []
        self.old_body.append(roster.create_player_row(False))
        self.old_body.append(roster.create_player_row(True))
        self.old_table = table(clazz='border mb-3', bcols=bcols, body=body)

        self.old_tables.append(state.create_head_table())
        self.old_tables.append(self.old_table)

    def get_old_body(self):
        return list(self.old_body)

    def get_live_tables(self):
        return self.live_tables

    def get_old_tables(self):
        return self.old_tables

    def get_summary(self):
        return list(self.summary)

    def reset_all(self):
        self.old_body = []
        self.summary = []

    def reset_old_body(self):
        self.old_body = []

    def reset_summary(self):
        self.summary = []


def create_tables():
    return Tables()
