#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class NotificationValue(Enum):
    NONE = 0
    BASE = 1
    EXPORT = 2
    SIM = 3
    UPLOAD = 4
    FILE = 5
    DOWNLOAD = 6
