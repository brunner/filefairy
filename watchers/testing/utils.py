#!/usr/bin/env python

import os


def assertEquals(actual, expected):
  if actual != expected:
    raise AssertionError(
        "Expected {0} to match {1}, but it didn't.".format(expected, actual))


def assertNotEquals(actual, expected):
  if actual == expected:
    raise AssertionError(
        "Expected {0} to not match {1}, but it did.".format(expected, actual))
