#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import pytz
import re

_est = pytz.timezone('America/New_York')


def datetime_datetime(*args):
    return _est.localize(datetime.datetime(*args))


def datetime_now():
    return _est.localize(datetime.datetime.now())


def decode_datetime(s):
    return _est.localize(
        datetime.datetime(*map(int, re.findall('\d+', s[:-6]))))


def encode_datetime(d):
    return d.isoformat()


def suffix(day):
    return 'th' if 11 <= day <= 13 else {
        1: 'st',
        2: 'nd',
        3: 'rd'
    }.get(day % 10, 'th')
