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
    f.write('A 1 1 57 0 42 0 C\n' +
            'B 1 2 45 0 32 0 E\n' +
            'C 2 1 A 0 59 0 G\n' +
            'D 2 1 47 0 54 0 G\n' +
            'E 2 2 B 0 51 0 H\n' +
            'F 2 2 56 0 55 0 H\n' +
            'G 3 1 C 0 D 0 I\n' +
            'H 3 2 E 0 F 0 I\n' +
            'I 4 0 G 0 H 0 X')

  chat_post_message('testing', 'Run setup.')
  time.sleep(6)

  assert_equals(appTest.settings['playoffs'], True)
  assert_equals(appTest.settings['standings'], False)

  assert_equals(subprocess.check_output(['rm', se_o]), '')
  assert_equals(subprocess.check_output(['rm', p_o]), '')

  appTest.handle_close()
  t1.join()


if __name__ == '__main__':
  test()
