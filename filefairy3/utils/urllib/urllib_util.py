#!/usr/bin/env python

import urllib2


def urlopen(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return ''
