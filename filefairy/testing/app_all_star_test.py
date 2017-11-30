#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from slack_api import chat_post_message
from utils import assert_equals


inpt = ['07/27/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|AL 4, NL 3>*']

outpt = '07/27/2021\n' + \
        '<https://game_box_0.html|AL 4, NL 3>'


def test():
  appTest = AppTest(standings_in='data/standings_in.txt')
  appTest.setup()

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  for i in inpt:
    chat_post_message('testing', i)
  time.sleep(2)

  assert_equals(appTest.process_final_scores(), outpt)
  assert_equals(appTest.process_records(), '')

  appTest.handle_close()
  t1.join()


if __name__ == '__main__':
  test()
