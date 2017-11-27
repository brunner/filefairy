#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from utils import assert_equals


inpt = ['data/exports1.html', 'data/exports2.html']
outp = ['Saturday January 14, 2017 13:01:09 EST', 'Tuesday January 17, 2017 09:03:12 EST']


def test_get_file_date():
  appTest = AppTest(file_url=inpt[0])
  appTest.setup()

  page = appTest.get_page(inpt[0])
  assert_equals(appTest.get_file_date(page), outp[0])

  page = appTest.get_page(inpt[1])
  assert_equals(appTest.get_file_date(page), outp[1])


def test_update_league_file():
  appTest = AppTest(file_url=inpt[0])
  appTest.setup()

  appTest.update_league_file()
  assert_equals(appTest.file_date, outp[0])

  appTest.file_url = inpt[1]
  appTest.update_league_file()
  assert_equals(appTest.file_date, outp[1])


def test_watch():
  appTest = AppTest(file_url=inpt[0])
  appTest.setup()

  t1 = threading.Thread(target=appTest.watch)
  t1.start()
  time.sleep(2)

  assert_equals(appTest.file_date, outp[0])

  appTest.file_url = inpt[1]
  time.sleep(2)

  assert_equals(appTest.file_date, outp[1])


if __name__ == '__main__':
  test_get_file_date()
  test_update_league_file()
  test_watch()
