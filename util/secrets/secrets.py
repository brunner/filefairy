#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def brunnerj():
    return 'xoxp-14121060643-89749308405-363014921589-b4dd84438862356ad102bc20e4c0d59e'


def filefairy():
    return 'x0xb-130692251397-IOiR7neeMTkGY0rMCjCa7YMv'


def server():
    return '45.79.186.214'


def secrets_sub(s):
    _ = {brunnerj(): 'brunnerj', filefairy(): 'filefairy', server(): 'server'}
    pattern = '|'.join(list(_.keys()))
    return re.sub(pattern, lambda m: _.get(m.group()), s)
