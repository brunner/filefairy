#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class Notify(Enum):
    BASE = 1

    EXPORTS_EMAILS = 2

    FAIRYLAB_DAY = 3

    LEAGUEFILE_DOWNLOAD = 4

    LEAGUEFILE_FINISH = 5

    LEAGUEFILE_START = 6

    LEAGUEFILE_YEAR = 7

    STATSPLUS_SIM = 8

    OTHER = 9
