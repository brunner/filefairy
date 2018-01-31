#!/usr/bin/env python

import subprocess


def check_output(cmd):
  try:
    return subprocess.check_output(cmd)
  except:
    return ''
