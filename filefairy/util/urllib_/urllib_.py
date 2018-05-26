#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse as parse
import urllib.request as request


def urlopen(url, params={}):
    try:
        data = parse.urlencode(params).encode('utf-8')
        with request.urlopen(url, data=data, timeout=8) as f:
            return f.read()
    except:
        return b''
