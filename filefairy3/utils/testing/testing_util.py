#!/usr/bin/env python

import json


def write(fname, data):
    with open(fname, 'r+') as f:
        original = json.loads(f.read())

        f.seek(0)
        f.write(json.dumps(data))
        f.truncate()

        return original
