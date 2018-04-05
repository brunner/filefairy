#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


def hash_file(fname):
    h = hashlib.sha256()
    with open(fname, 'rb', buffering=0) as f:
        for b in iter(lambda: f.read(128 * 1024), b''):
            h.update(b)
    return h.hexdigest()
