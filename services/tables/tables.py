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
        self.live_head = []
        self.live_body = []
        self.live_foot = []

        self.old_body = []
        self.old_table = table()
        self.old_tables = []
        self.summary = []

    def append_all(self):
        for r in self.old_body:
            tbody(self.old_table, r)

    def append_live_head(self, t):
        self.live_head.append(t)

    def append_old_body(self, r):
        self.old_body.append(r)

    def append_summary(self, s):
        self.summary.append(s)

    def create_old_table(self, roster, state):
        self.old_tables.append(state.create_old_head_table())

        body, self.old_body = list(self.old_body), []
        if body:
            t = table(clazz='border border-bottom-0', body=body)
            self.old_tables.append(t)
        self.old_tables.append(roster.create_old_pitcher_table())
        self.old_tables.append(roster.create_old_batter_table())

        bcols = [col(), col(clazz='w-50p text-right')]
        self.old_table = table(clazz='border mb-3', bcols=bcols, body=[])
        self.old_tables.append(self.old_table)

    def get_old_body(self):
        return list(self.old_body)

    def get_live_tables(self):
        return self.live_head + [
            table(
                clazz='table-fixed border mb-3',
                bcols=[col(), col(clazz='w-50p text-right')],
                body=self.live_body),
            table(clazz='border mb-3', body=self.live_foot),
        ]

    def get_old_tables(self):
        return self.old_tables

    def get_summary(self):
        return list(self.summary)

    def prepend_live_body(self, r):
        self.live_body.insert(0, r)

    def prepend_live_foot(self, r):
        self.live_foot.insert(0, r)

    def reset_all(self):
        self.old_body = []
        self.summary = []

    def reset_old_body(self):
        self.old_body = []

    def reset_summary(self):
        self.summary = []


def create_tables():
    return Tables()
