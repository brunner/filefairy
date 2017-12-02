#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from slack_api import chat_post_message
from utils import assert_equals


inpt = ['07/27/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|American League 4, National League 3>*',
        '07/28/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Atlanta 3, Colorado 1>*']

outpt = '07/27/2021\n' + \
        '<https://game_box_0.html|American League 4, National League 3>\n' + \
        '07/28/2021\n' + \
        '<https://game_box_0.html|Atlanta 3, Colorado 1>'

rcrds = 'NL East\n:braves: 1-0\n\nNL West\n:rox: 0-1'


def test():
  appTest = AppTest()
  appTest.setup()

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  for i in inpt:
    chat_post_message('testing', i)
  time.sleep(2)

  assert_equals(appTest.process_final_scores(), outpt)
  assert_equals(appTest.process_records(), rcrds)

  appTest.handle_close()
  t1.join()


if __name__ == '__main__':
  test()
