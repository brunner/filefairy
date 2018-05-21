#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse as parse
import urllib.request as request


def _create_request(url, params):
    return request.Request(url, parse.urlencode(params))


def urlopen(url, params={}):
    try:
        data = parse.urlencode(params).encode('utf-8')
        with request.urlopen(url, data=data, timeout=8) as f:
            return f.read().decode('utf-8')
    except Exception as e:
        print(e)
        return ''
