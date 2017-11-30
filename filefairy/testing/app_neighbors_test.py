#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from slack_api import chat_post_message
from utils import assert_equals


inpt = ['07/19/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Chicago 4, Baltimore 1>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/19/2021\n' +
        'Chicago White Sox               1\nBaltimore Orioles               0```',
        '07/20/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Baltimore 3, Chicago 0>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/20/2021\n' +
        'Baltimore Orioles               1\nChicago White Sox               1```',
        '07/21/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Chicago 7, Baltimore 4>*\n' +
        '*<https://game_box_0.html|Chicago 10, Baltimore 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/21/2021\n' +
        'Chicago White Sox               3\nBaltimore Orioles               1```',
        '07/22/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Baltimore 13, Chicago 4>*\n' +
        '*<https://game_box_0.html|Baltimore 1, Chicago 0>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/22/2021\n' +
        'Baltimore Orioles               3\nChicago White Sox               3```',
        '07/23/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Chicago 8, Baltimore 1>*\n' +
        '*<https://game_box_0.html|Baltimore 3, Chicago 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/23/2021\n' +
        'Baltimore Orioles               4\nChicago White Sox               4```',
        '07/24/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Chicago 4, Arizona 3>*\n' +
        '*<https://game_box_0.html|Chicago 11, Baltimore 7>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/24/2021\n' +
        'Chicago White Sox               5\nBaltimore Orioles               4\n' +
        'Chicago Cubs                    1\nArizona Diamondbacks            0```',
        '07/25/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Arizona 4, Chicago 0>*\n' +
        '*<https://game_box_0.html|Baltimore 9, Chicago 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/25/2021\n' +
        'Baltimore Orioles               5\nChicago White Sox               5\n' +
        'Arizona Diamondbacks            1\nChicago Cubs                    1```',
        '07/26/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Baltimore 6, Chicago 3>*\n' +
        '*<https://game_box_0.html|Chicago 2, Arizona 1>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/26/2021\n' +
        'Baltimore Orioles               6\nChicago White Sox               5\n' +
        'Chicago Cubs                    2\nArizona Diamondbacks            1```',
        '07/27/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Chicago 4, Arizona 2>*\n' +
        '*<https://game_box_0.html|Chicago 7, Arizona 6>*\n' +
        '*<https://game_box_0.html|Chicago 5, Baltimore 3>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/27/2021\n' +
        'Baltimore Orioles               6\nChicago White Sox               6\n' +
        'Chicago Cubs                    4\nArizona Diamondbacks            1```',
        '07/28/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Baltimore 6, Chicago 1>*\n' +
        '*<https://game_box_0.html|Chicago 10, Arizona 3>*\n' +
        '*<https://game_box_0.html|Chicago 9, Arizona 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/28/2021\n' +
        'Baltimore Orioles               7\nChicago Cubs                    6\n' +
        'Chicago White Sox               6\nArizona Diamondbacks            1```',
        '07/29/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Baltimore 8, Chicago 7>*\n' +
        '*<https://game_box_0.html|Chicago 1, Arizona 0>*\n' +
        '*<https://game_box_0.html|Chicago 4, Baltimore 3>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/29/2021\n' +
        'Baltimore Orioles               8\nChicago Cubs                    7\n' +
        'Chicago White Sox               7\nArizona Diamondbacks            1```',
        '07/30/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Boston 3, Chicago 1>*\n' +
        '*<https://game_box_0.html|Chicago 6, Atlanta 0>*\n' +
        '*<https://game_box_0.html|Chicago 7, Boston 5>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/30/2021\n' +
        'Baltimore Orioles               8\nChicago Cubs                    8\n' +
        'Chicago White Sox               8\nArizona Diamondbacks            1\n' +
        'Boston Red Sox                  1\nAtlanta Braves                  0```']

outp = ['AL East\n:orioles: 0-1\n\nAL Central\n:whitesox: 1-0',
        'AL East\n:orioles: 1-1\n\nAL Central\n:whitesox: 1-1',
        'AL East\n:orioles: 1-3\n\nAL Central\n:whitesox: 3-1',
        'AL East\n:orioles: 3-3\n\nAL Central\n:whitesox: 3-3',
        'AL East\n:orioles: 4-4\n\nAL Central\n:whitesox: 4-4',
        'AL East\n:orioles: 4-5\n\nAL Central\n:whitesox: 5-4\n\n' +
        'NL Central\n:cubbies: 1-0\n\nNL West\n:dbacks: 0-1',
        'AL East\n:orioles: 5-5\n\nAL Central\n:whitesox: 5-5\n\n' +
        'NL Central\n:cubbies: 1-1\n\nNL West\n:dbacks: 1-1',
        'AL East\n:orioles: 6-5\n\nAL Central\n:whitesox: 5-6\n\n' +
        'NL Central\n:cubbies: 2-1\n\nNL West\n:dbacks: 1-2',
        'AL East\n:orioles: 6-6\n\nAL Central\n:whitesox: 6-6\n\n' +
        'NL Central\n:cubbies: 4-1\n\nNL West\n:dbacks: 1-4',
        'AL East\n:orioles: 7-6\n\nAL Central\n:whitesox: 6-7\n\n' +
        'NL Central\n:cubbies: 6-1\n\nNL West\n:dbacks: 1-6',
        'AL East\n:orioles: 8-7\n\nAL Central\n:whitesox: 7-8\n\n' +
        'NL Central\n:cubbies: 7-1\n\nNL West\n:dbacks: 1-7',
        'AL East\n:orioles: 8-7 :separator: :redsox: 1-1\n\n' +
        'AL Central\n:whitesox: 8-8\n\nNL East\n:braves: 0-1\n\n' +
        'NL Central\n:cubbies: 8-1\n\nNL West\n:dbacks: 1-7\n\n' +
        '_Unhandled loss for Chicago._']


def test():
  appTest = AppTest()
  appTest.setup()

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  for i in range(0, len(inpt), 2):
    chat_post_message('testing', inpt[i])
    chat_post_message('testing', inpt[i + 1])

    time.sleep(2)
    appTest.process_final_scores()
    assert_equals(appTest.process_records(), outp[i / 2])

  time.sleep(2)
  appTest.handle_close()
  t1.join()


if __name__ == '__main__':
  test()
