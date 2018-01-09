#!/usr/bin/env python

import json
import os
import subprocess
import threading
import time

from app_test import AppTest
from slack_api import chat_post_message
from utils import assert_equals


def test():
  appTest = AppTest(settings_in='data/settings_in.txt')
  appTest.setup()

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  assert_equals(appTest.settings['playoffs'], False)
  assert_equals(appTest.settings['standings'], True)

  se_o = os.path.join(appTest.get_path(), 'data/settings_over.txt')
  with open(se_o, 'w') as f:
    f.write(json.dumps({'playoffs': True, 'standings': False}))

  p_o = os.path.join(appTest.get_path(), 'data/playoffs_over.txt')
  with open(p_o, 'w') as f:
    f.write('A 1 1 1 57 42 0 0 C\n' +
            'B 1 1 2 45 32 0 0 E\n' +
            'C 2 3 1 A 59 0 0 G\n' +
            'D 2 3 1 47 54 0 0 G\n' +
            'E 2 3 2 B 51 0 0 H\n' +
            'F 2 3 2 56 55 0 0 H\n' +
            'G 3 4 1 C D 0 0 I\n' +
            'H 3 4 2 E F 0 0 I\n' +
            'I 4 4 0 G H 0 0 X')

  chat_post_message('testing', 'Run app setup.')
  chat_post_message('testing', 'Run app status report.')
  time.sleep(6)

  assert_equals(appTest.settings['playoffs'], True)
  assert_equals(appTest.settings['standings'], False)

  assert_equals(subprocess.check_output(['rm', se_o]), '')
  assert_equals(subprocess.check_output(['rm', p_o]), '')

  appTest.handle_close()
  t1.join()


if __name__ == '__main__':
  test()
