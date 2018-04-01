#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class ActivityEnum(Enum):
    NONE = 0
    BASE = 1
    EXPORT = 2
    SIM = 3
    FILE = 4
    DOWNLOAD = 5
