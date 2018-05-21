#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re


def decode_datetime(s):
    return datetime.datetime(*map(int, re.findall('\d+', s)))


def encode_datetime(d):
    return d.isoformat()


def suffix(day):
    return 'th' if 11 <= day <= 13 else {
        1: 'st',
        2: 'nd',
        3: 'rd'
    }.get(day % 10, 'th')
