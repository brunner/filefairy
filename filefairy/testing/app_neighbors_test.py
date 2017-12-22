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
        'Boston Red Sox                  1\nAtlanta Braves                  0```',
        '07/31/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Boston 5, Chicago 1>*\n' +
        '*<https://game_box_0.html|Chicago 2, Atlanta 1>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/31/2021\n' +
        'Chicago Cubs                    9\nBaltimore Orioles               8\n' +
        'Chicago White Sox               8\nBoston Red Sox                  2\n' +
        'Arizona Diamondbacks            1\nAtlanta Braves                  0```',
        '08/01/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Atlanta 6, Chicago 4>*\n' +
        '*<https://game_box_0.html|Boston 8, Chicago 0>*\n' +
        '*<https://game_box_0.html|Chicago 3, Boston 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 08/01/2021\n' +
        'Chicago Cubs                    9\nChicago White Sox               9\n' +
        'Baltimore Orioles               8\nBoston Red Sox                  2\n' +
        'Arizona Diamondbacks            1\nAtlanta Braves                  1```',
        '08/02/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Atlanta 3, Chicago 2>*\n' +
        '*<https://game_box_0.html|Chicago 3, Boston 0>*\n' +
        '*<https://game_box_0.html|Chicago 8, Boston 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 08/02/2021\n' +
        'Chicago White Sox              11\nChicago Cubs                    9\n' +
        'Baltimore Orioles               8\nAtlanta Braves                  2\n' +
        'Boston Red Sox                  2\nArizona Diamondbacks            1```',
        '08/03/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Baltimore 5, Chicago 1>*\n' +
        '*<https://game_box_0.html|Baltimore 8, Chicago 7>*\n' +
        '*<https://game_box_0.html|Arizona 10, Chicago 0>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 08/03/2021\n' +
        'Chicago White Sox              11\nBaltimore Orioles              10\n' +
        'Chicago Cubs                    9\nArizona Diamondbacks            2\n' +
        'Atlanta Braves                  2\nBoston Red Sox                  2```',
        '08/04/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Baltimore 6, Chicago 1>*\n' +
        '*<https://game_box_0.html|Chicago 2, Arizona 1>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 08/04/2021\n' +
        'Baltimore Orioles              11\nChicago White Sox              11\n' +
        'Chicago Cubs                   10\nArizona Diamondbacks            2\n' +
        'Atlanta Braves                  2\nBoston Red Sox                  2```',
        '08/05/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Chicago 10, Cleveland 3>*\n' +
        '*<https://game_box_0.html|Chicago 2, Cleveland 0>*\n' +
        '*<https://game_box_0.html|Chicago 4, Cincinnati 3>*\n' +
        '*<https://game_box_0.html|Chicago 8, Cincinnati 6>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 08/05/2021\n' +
        'Chicago White Sox              13\nChicago Cubs                   12\n' +
        'Baltimore Orioles              11\nArizona Diamondbacks            2\n' +
        'Atlanta Braves                  2\nBoston Red Sox                  2\n' +
        'Cincinnati Reds                 0\nCleveland Indians               0```',
        '08/06/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Chicago 13, Cleveland 7>*\n' +
        '*<https://game_box_0.html|Chicago 7, Cleveland 3>*\n' +
        '*<https://game_box_0.html|Chicago 8, Cincinnati 1>*\n' +
        '*<https://game_box_0.html|Cincinnati 2, Chicago 0>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 08/06/2021\n' +
        'Chicago White Sox              15\nChicago Cubs                   13\n' +
        'Baltimore Orioles              11\nArizona Diamondbacks            2\n' +
        'Atlanta Braves                  2\nBoston Red Sox                  2\n' +
        'Cincinnati Reds                 1\nCleveland Indians               0```',
        '08/07/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Chicago 4, Cleveland 2>*\n' +
        '*<https://game_box_0.html|Chicago 7, Cleveland 1>*\n' +
        '*<https://game_box_0.html|Cincinnati 3, Chicago 2>*\n' +
        '*<https://game_box_0.html|Cincinnati 9, Chicago 5>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 08/07/2021\n' +
        'Chicago White Sox              17\nChicago Cubs                   13\n' +
        'Baltimore Orioles              11\nCincinnati Reds                 3\n' +
        'Arizona Diamondbacks            2\nAtlanta Braves                  2\n' +
        'Boston Red Sox                  2\nCleveland Indians               0```',
        '08/08/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Chicago 6, Cincinnati 2>*\n' +
        '*<https://game_box_0.html|Chicago 2, Cleveland 1>*\n' +
        '*<https://game_box_0.html|Cincinnati 10, Chicago 6>*\n' +
        '*<https://game_box_0.html|Cleveland 7, Chicago 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 08/08/2021\n' +
        'Chicago White Sox              18\nChicago Cubs                   14\n' +
        'Baltimore Orioles              11\nCincinnati Reds                 4\n' +
        'Arizona Diamondbacks            2\nAtlanta Braves                  2\n' +
        'Boston Red Sox                  2\nCleveland Indians               1```',
        '08/09/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Chicago 7, Cleveland 4>*\n' +
        '*<https://game_box_0.html|Cincinnati 6, Chicago 4>*\n' +
        '*<https://game_box_0.html|Cincinnati 8, Chicago 7>*\n' +
        '*<https://game_box_0.html|Cleveland 3, Chicago 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 08/09/2021\n' +
        'Chicago White Sox              19\nChicago Cubs                   14\n' +
        'Baltimore Orioles              11\nCincinnati Reds                 6\n' +
        'Arizona Diamondbacks            2\nAtlanta Braves                  2\n' +
        'Boston Red Sox                  2\nCleveland Indians               2```',
        '08/10/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Cincinnati 7, Chicago 6>*\n' +
        '*<https://game_box_0.html|Cincinnati 2, Chicago 0>*\n' +
        '*<https://game_box_0.html|Cleveland 6, Chicago 2>*\n' +
        '*<https://game_box_0.html|Cleveland 4, Chicago 3>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 08/10/2021\n' +
        'Chicago White Sox              19\nChicago Cubs                   14\n' +
        'Baltimore Orioles              11\nCincinnati Reds                 8\n' +
        'Cleveland Indians               4\nArizona Diamondbacks            2\n' +
        'Atlanta Braves                  2\nBoston Red Sox                  2```']

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
        '_Unhandled loss for Chicago._',
        'AL East\n:redsox: 2-1 :separator: :orioles: 8-7\n\n' +
        'AL Central\n:whitesox: 8-10\n\nNL East\n:braves: 0-2\n\n' +
        'NL Central\n:cubbies: 9-1\n\nNL West\n:dbacks: 1-7',
        'AL East\n:redsox: 3-2 :separator: :orioles: 8-7\n\n' +
        'AL Central\n:whitesox: 9-11\n\nNL East\n:braves: 1-2\n\n' +
        'NL Central\n:cubbies: 9-2\n\nNL West\n:dbacks: 1-7',
        'AL East\n:orioles: 8-7 :separator: :redsox: 3-4\n\n' +
        'AL Central\n:whitesox: 11-11\n\nNL East\n:braves: 2-2\n\n' +
        'NL Central\n:cubbies: 9-3\n\nNL West\n:dbacks: 1-7',
        'AL East\n:orioles: 10-7 :separator: :redsox: 3-4\n\n' +
        'AL Central\n:whitesox: 11-12\n\nNL East\n:braves: 2-2\n\n' +
        'NL Central\n:cubbies: 9-4\n\nNL West\n:dbacks: 2-7\n\n' +
        '_Unhandled loss for Chicago._',
        'AL East\n:orioles: 11-7 :separator: :redsox: 3-4\n\n' +
        'AL Central\n:whitesox: 11-14\n\nNL East\n:braves: 2-2\n\n' +
        'NL Central\n:cubbies: 10-4\n\nNL West\n:dbacks: 2-8',
        'AL East\n:orioles: 11-7 :separator: :redsox: 3-4\n\n' +
        'AL Central\n:whitesox: 13-14 :separator: :indians: 0-2\n\n' +
        'NL East\n:braves: 2-2\n\nNL Central\n:cubbies: 12-4 ' +
        ':separator: :reds: 0-2\n\nNL West\n:dbacks: 2-8',
        'AL East\n:orioles: 11-7 :separator: :redsox: 3-4\n\n' +
        'AL Central\n:whitesox: 15-14 :separator: :indians: 0-4\n\n' +
        'NL East\n:braves: 2-2\n\nNL Central\n:cubbies: 13-5 ' +
        ':separator: :reds: 1-3\n\nNL West\n:dbacks: 2-8',
        'AL East\n:orioles: 11-7 :separator: :redsox: 3-4\n\n' +
        'AL Central\n:whitesox: 17-14 :separator: :indians: 0-6\n\n' +
        'NL East\n:braves: 2-2\n\nNL Central\n:cubbies: 13-7 ' +
        ':separator: :reds: 3-3\n\nNL West\n:dbacks: 2-8',
        'AL East\n:orioles: 11-7 :separator: :redsox: 3-4\n\n' +
        'AL Central\n:whitesox: 18-15 :separator: :indians: 1-7\n\n' +
        'NL East\n:braves: 2-2\n\nNL Central\n:cubbies: 14-8 ' +
        ':separator: :reds: 4-4\n\nNL West\n:dbacks: 2-8',
        'AL East\n:orioles: 11-7 :separator: :redsox: 3-4\n\n' +
        'AL Central\n:whitesox: 19-16 :separator: :indians: 2-8\n\n' +
        'NL East\n:braves: 2-2\n\nNL Central\n:cubbies: 14-10 ' +
        ':separator: :reds: 6-4\n\nNL West\n:dbacks: 2-8',
        'AL East\n:orioles: 11-7 :separator: :redsox: 3-4\n\n' +
        'AL Central\n:whitesox: 19-18 :separator: :indians: 4-8\n\n' +
        'NL East\n:braves: 2-2\n\nNL Central\n:reds: 8-4 ' +
        ':separator: :cubbies: 14-12\n\nNL West\n:dbacks: 2-8']


def test():
  appTest = AppTest(settings_in='data/settings_in.txt')
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
