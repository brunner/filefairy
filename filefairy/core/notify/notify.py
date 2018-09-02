#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class Notify(Enum):
    BASE = 1

    EXPORTS_EMAILS = 2

    FAIRYLAB_DAY = 3

    FAIRYLAB_DEPLOY = 4

    LEAGUEFILE_DOWNLOAD = 5

    LEAGUEFILE_FINISH = 6

    LEAGUEFILE_START = 7

    LEAGUEFILE_YEAR = 8

    STATSPLUS_SIM = 9

    OTHER = 10
