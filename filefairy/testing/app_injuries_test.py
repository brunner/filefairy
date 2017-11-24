#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from logger import TestLogger
from slack_api import SlackApi
from utils import assertEquals


inpt = ['03/21/2021 RP <https://player_33610.html|Drew Pomeranz> was injured ' +
        'while pitching (Baltimore @ Seattle)',
        '03/21/2021 LF <https://player_37732.html|Alexis Rivera> was injured ' +
        'on a defensive play (Cleveland @ Toronto)',
        '03/21/2021 Rain delay of 16 minutes in the 7th inning. ' +
        'SS <https://player_39374.html|Amed Rosario> was injured ' +
        'in a collision at a base (Kansas City @ Detroit)',
        '03/21/2021 3B <https://player_31259.html|Matt Davidson> was injured ' +
        'during a surprise event (Chicago @ Texas)']

outpt = 'Injuries:\n' + \
        '<https://player_33610.html|Drew Pomeranz> (pitching)\n' + \
        '<https://player_37732.html|Alexis Rivera> (defensive play)\n' + \
        '<https://player_39374.html|Amed Rosario> (collision at a base)\n' + \
        '<https://player_31259.html|Matt Davidson> (during a surprise event)'


def test():
  logger = TestLogger()
  slackApi = SlackApi(logger)
  appTest = AppTest(logger, slackApi)

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  for injury in inpt:
    slackApi.chatPostMessage('testing', injury)

  appTest.handleClose()
  time.sleep(1)
  t1.join()

  assertEquals(appTest.processInjuries(), outpt)


if __name__ == '__main__':
  test()
