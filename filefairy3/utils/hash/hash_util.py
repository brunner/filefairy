#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib

_bufsize = 65536


def hash_file(fname):
    h = hashlib.sha256()
    with open(fname, 'rb') as f:
        while True:
            data = f.read(_bufsize)
            if not data:
                break
            h.update(data)
    return h.hexdigest()
