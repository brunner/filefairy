#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import TestLogger
from utils import assertEquals


def testLogger():
  logger = TestLogger()

  logger.log("foo")
  logger.log("bar")
  logger.log("baz")

  logs = logger.dump()
  assertEquals(logs[0], "[0:0:0] foo")
  assertEquals(logs[1], "[0:0:0] bar")
  assertEquals(logs[2], "[0:0:0] baz")


if __name__ == "__main__":
  testLogger()

  print "Passed."
