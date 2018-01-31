#!/usr/bin/env python


def overwrite(fname, s):
  with open(fname, 'r+') as f:
    original = f.read()
    f.seek(0)
    f.write(s)
    f.truncate()
    return original
