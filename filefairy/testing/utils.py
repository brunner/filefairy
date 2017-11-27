#!/usr/bin/env python


def assert_equals(actual, expected):
  if actual != expected:
    raise AssertionError("Expected {0} to match {1}, but it didn't.".format(expected, actual))
