#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def filefairy():
    return 'xoxb-130692251397-LkJyQ6NztPuDVAJ7P6xDboHo'


def server():
    return '45.79.186.214'


def secrets_sub(s):
    _ = {filefairy(): 'filefairy', server(): 'server'}
    pattern = '|'.join(list(_.keys()))
    return re.sub(pattern, lambda m: _.get(m.group()), s)
