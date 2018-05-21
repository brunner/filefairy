#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib


def create_request(url, params):
    return urllib.request.Request(url, urllib.parse.urlencode(params))


def urlopen(url):
    try:
        return urllib.request.urlopen(url, timeout=8).read()
    except:
        return ''
