#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from utils import assert_equals


inpt = ['exports1.html', 'exports2.html']
outp = ['Saturday January 14, 2017 13:01:09 EST', 'Tuesday January 17, 2017 09:03:12 EST']


def test():
  appTest = AppTest()
  page = appTest.get_page(inpt[0])
  assert_equals(appTest.get_file_date(page), outp[0])

  page = appTest.get_page(inpt[1])
  assert_equals(appTest.get_file_date(page), outp[1])


if __name__ == '__main__':
  test()
