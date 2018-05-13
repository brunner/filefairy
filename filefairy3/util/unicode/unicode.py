#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata


def deunicode(text, errors='replace'):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', errors)
    text = text.decode("utf-8")
    return str(text)
