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


def getExportUrls():
  path = "http://brunnerj.com/orangeandblueleague/"
  files = [
      "export_01142017_1.html",         # 0. Initial exports page.
      "export_01142017_2.html",         # 1. League file date has not changed.
      "export_01172017_1.html",         # 2. League file date has changed.
  ]
  return [os.path.join(path, fi) for fi in files]


def getSimUrls():
  path = "http://brunnerj.com/orangeandblueleague/"
  files = [
      "sim_09052018_1.html",            # 0. Initial sim page.
      "sim_09052018_2.html",            # 1. Same date. No new final games.
      "sim_09052018_3.html",            # 2. Same date. One new final game.
      "sim_09092018_1.html",            # 3. Different date, partially loaded.
      "sim_09092018_2.html",            # 4. Fully loaded.
      "sim_09092018_3.html",            # 5. Partially loaded again.
      ]
  return [os.path.join(path, fi) for fi in files]