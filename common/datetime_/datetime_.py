#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import pytz
import re

_est = pytz.timezone('America/New_York')
_pst = pytz.timezone('America/Los_Angeles')


def datetime_as_pst(d):
    return d.astimezone(_pst)


def datetime_datetime_est(*args):
    return _est.localize(datetime.datetime(*args))


def datetime_datetime_pst(*args):
    return _pst.localize(datetime.datetime(*args))


def datetime_now():
    return _pst.localize(datetime.datetime.now())


def decode_datetime(s):
    return datetime_datetime_pst(*map(int, re.findall('\d+', s[:-6])))


def encode_datetime(d):
    return datetime_as_pst(d).isoformat()


def suffix(day):
    return 'th' if 11 <= day <= 13 else {
        1: 'st',
        2: 'nd',
        3: 'rd'
    }.get(day % 10, 'th')


def timedelta(then, now):
    diff = now - then
    s, d = diff.seconds, diff.days

    if s < 0 or d < 0:
        return timedelta(now, then)

    if d > 0:
        s += 86400 * d

    h, m = s // 3600, (s // 60) % 60
    hm = []
    if h > 0:
        hm.append('{}h'.format(h))
    hm.append('{}m'.format(m))

    return ' '.join(hm)


def timestamp(date):
    return date.strftime('%H:%M:%S %Z (%Y-%m-%d)')
