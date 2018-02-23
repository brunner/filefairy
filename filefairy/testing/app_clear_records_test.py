#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from slack_api import chat_post_message
from utils import assert_equals


inpt = ['07/27/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Colorado 4, Atlanta 3>*',
        '07/28/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Atlanta 3, Colorado 1>*']

outp = ['07/27/2021\n' +
        '<https://game_box_0.html|Colorado 4, Atlanta 3>',
        '07/28/2021\n' +
        '<https://game_box_0.html|Atlanta 3, Colorado 1>']

rcds = ['NL East\n:braves: 0-1\n\nNL West\n:rox: 1-0',
        'NL East\n:braves: 1-0\n\nNL West\n:rox: 0-1']

def test():
  appTest = AppTest(settings_in='data/settings_in.txt')
  appTest.setup()

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  for j, i in enumerate(inpt):
    chat_post_message('testing', i)
    time.sleep(2)
    assert_equals(appTest.process_final_scores(), outp[j])
    assert_equals(appTest.process_records(), rcds[j])

  appTest.handle_close()
  t1.join()


if __name__ == '__main__':
  test()
