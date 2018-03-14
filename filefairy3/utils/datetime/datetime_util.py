#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re


def decode_datetime(s):
    return datetime.datetime(*map(int, re.findall('\d+', s)))


def encode_datetime(d):
    return d.isoformat()
