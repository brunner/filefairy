#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2


def create_request(url, params):
    return urllib2.Request(url, urllib.urlencode(params))


def urlopen(url):
    try:
        return urllib2.urlopen(url, timeout=8).read()
    except:
        return ''
