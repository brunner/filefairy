#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class NotifyValue(Enum):
    BASE = 1

    DOWNLOAD_FINISH = 2

    EXPORTS_EMAILS = 3

    FAIRYLAB_DAY = 4

    LEAGUEFILE_FINISH = 5

    LEAGUEFILE_START = 6

    STATSPLUS_SIM = 7

    OTHER = 8
