#!/usr/bin/env python

from difflib import ndiff


def assert_equals(actual, expected):
  if actual != expected:
    diff = ''.join(ndiff(actual, expected))
    raise AssertionError("Actual did not match expected:\n{}".format(diff))
