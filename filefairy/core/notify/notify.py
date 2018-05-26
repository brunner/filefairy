#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class Notify(Enum):
    BASE = 1

    DOWNLOAD_FINISH = 2

    DOWNLOAD_YEAR = 3

    EXPORTS_EMAILS = 4

    FAIRYLAB_DAY = 5

    LEAGUEFILE_FINISH = 6

    LEAGUEFILE_START = 7

    STATSPLUS_SIM = 8

    OTHER = 9
