#!/usr/bin/env python


def assertEquals(actual, expected):
  if actual != expected:
    raise AssertionError(
        "Expected {0} to match {1}, but it didn't.".format(expected, actual))


def assertNotEquals(actual, expected):
  if actual == expected:
    raise AssertionError(
        "Expected {0} to not match {1}, but it did.".format(expected, actual))

def assertContains(iterable, element):
  if element not in iterable:
    raise AssertionError(
        "Expected {0} to contain {1}, but it didn't.".format(iterable, element))