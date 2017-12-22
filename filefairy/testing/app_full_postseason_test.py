#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from slack_api import chat_post_message
from utils import assert_equals


wcinpt = ['10/01/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Tampa Bay 9, Houston 6>*',
          '10/02/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Atlanta 5, Los Angeles 3>*']

wcoutpt = ['AL Wild Card            |  W\n' +
           '------------------------|----\n' +
           'Tampa Bay Rays          |  1\n' +
           'Houston Astros          |  0\n\n' +
           'NL Wild Card            |  W\n' +
           '------------------------|----\n' +
           'Los Angeles Dodgers     |  0\n' +
           'Atlanta Braves          |  1',
           'A 1 1 57 1 42 0 C\n' +
           'B 1 2 45 0 32 1 E\n' +
           'C 2 1 57 0 59 0 G\n' +
           'D 2 1 47 0 54 0 G\n' +
           'E 2 2 32 0 51 0 H\n' +
           'F 2 2 56 0 55 0 H\n' +
           'G 3 1 C 0 D 0 I\n' +
           'H 3 2 E 0 F 0 I\n' +
           'I 4 0 G 0 H 0 X\n']

dsinp1 = ['10/03/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Seattle 5, Minnesota 0>*\n' +
          '*<https://game_box_0.html|Toronto 12, Tampa Bay 9>*',
          '10/04/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Atlanta 5, Philadelphia 2>*\n' +
          '*<https://game_box_0.html|Minnesota 3, Seattle 2>*\n' +
          '*<https://game_box_0.html|San Francisco 8, St. Louis 2>*\n' +
          '*<https://game_box_0.html|Toronto 4, Tampa Bay 0>*',
          '10/05/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Philadelphia 7, Atlanta 1>*\n' +
          '*<https://game_box_0.html|St. Louis 6, San Francisco 4>*',
          '10/06/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Minnesota 4, Seattle 1>*\n' +
          '*<https://game_box_0.html|Tampa Bay 9, Toronto 5>*']

dsoutp1 = ['AL Division Series      |  W\n' +
           '------------------------|----\n' +
           'Tampa Bay Rays          |  1\n' +
           'Toronto Blue Jays       |  2\n\n' +
           'AL Division Series      |  W\n' +
           '------------------------|----\n' +
           'Minnesota Twins         |  2\n' +
           'Seattle Mariners        |  1\n\n' +
           'NL Division Series      |  W\n' +
           '------------------------|----\n' +
           'Atlanta Braves          |  1\n' +
           'Philadelphia Phillies   |  1\n\n' +
           'NL Division Series      |  W\n' +
           '------------------------|----\n' +
           'St. Louis Cardinals     |  1\n' +
           'San Francisco Giants    |  1',
           'A 1 1 57 1 42 0 C\n' +
           'B 1 2 45 0 32 1 E\n' +
           'C 2 1 57 1 59 2 G\n' +
           'D 2 1 47 2 54 1 G\n' +
           'E 2 2 32 1 51 1 H\n' +
           'F 2 2 56 1 55 1 H\n' +
           'G 3 1 C 0 D 0 I\n' +
           'H 3 2 E 0 F 0 I\n' +
           'I 4 0 G 0 H 0 X\n']

dsinp2 = ['10/07/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Philadelphia 7, Atlanta 2>*\n' +
          '*<https://game_box_0.html|Minnesota 8, Seattle 2>*\n' +
          '*<https://game_box_0.html|San Francisco 3, St. Louis 0>*\n' +
          '*<https://game_box_0.html|Toronto 7, Tampa Bay 6>*',
          '10/08/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Philadelphia 4, Atlanta 3>*\n' +
          '*<https://game_box_0.html|St. Louis 10, San Francisco 5>*',
          '10/10/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|San Francisco 1, St. Louis 0>*']

dsoutp2 = ['AL Division Series      |  W\n' +
           '------------------------|----\n' +
           'Tampa Bay Rays          |  1\n' +
           'Toronto Blue Jays       |  3\n\n' +
           'AL Division Series      |  W\n' +
           '------------------------|----\n' +
           'Minnesota Twins         |  3\n' +
           'Seattle Mariners        |  1\n\n' +
           'NL Division Series      |  W\n' +
           '------------------------|----\n' +
           'Atlanta Braves          |  1\n' +
           'Philadelphia Phillies   |  3\n\n' +
           'NL Division Series      |  W\n' +
           '------------------------|----\n' +
           'St. Louis Cardinals     |  2\n' +
           'San Francisco Giants    |  3',
           'A 1 1 57 1 42 0 C\n' +
           'B 1 2 45 0 32 1 E\n' +
           'C 2 1 57 1 59 3 G\n' +
           'D 2 1 47 3 54 1 G\n' +
           'E 2 2 32 1 51 3 H\n' +
           'F 2 2 56 2 55 3 H\n' +
           'G 3 1 47 0 59 0 I\n' +
           'H 3 2 55 0 51 0 I\n' +
           'I 4 0 G 0 H 0 X\n']

csinp1 = ['10/11/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Toronto 4, Minnesota 2>*',
          '10/12/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Philadelphia 4, San Francisco 1>*\n' +
          '*<https://game_box_0.html|Toronto 8, Minnesota 3>*',
          '10/13/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|San Francisco 5, Philadelphia 4>*',
          '10/14/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Toronto 6, Minnesota 3>*',
          '10/15/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Toronto 7, Minnesota 5>\n' +
          '*<https://game_box_0.html|San Francisco 4, Philadelphia 3>*']

csoutp1 = ['AL Championship Series  |  W\n' +
           '------------------------|----\n' +
           'Minnesota Twins         |  0\n' +
           'Toronto Blue Jays       |  4\n\n' +
           'NL Championship Series  |  W\n' +
           '------------------------|----\n' +
           'San Francisco Giants    |  2\n' +
           'Philadelphia Phillies   |  1',
           'A 1 1 57 1 42 0 C\n' +
           'B 1 2 45 0 32 1 E\n' +
           'C 2 1 57 1 59 3 G\n' +
           'D 2 1 47 3 54 1 G\n' +
           'E 2 2 32 1 51 3 H\n' +
           'F 2 2 56 2 55 3 H\n' +
           'G 3 1 47 0 59 4 I\n' +
           'H 3 2 55 2 51 1 I\n' +
           'I 4 0 59 0 H 0 X\n']

csinp2 = ['10/16/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Philadelphia 6, San Francisco 1>*',
          '10/17/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|San Francisco 8, Philadelphia 4>*',
          '10/19/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|San Francisco 8, Philadelphia 2>*']

csoutp2 = ['AL Championship Series  |  W\n' +
           '------------------------|----\n' +
           'Minnesota Twins         |  0\n' +
           'Toronto Blue Jays       |  4\n\n' +
           'NL Championship Series  |  W\n' +
           '------------------------|----\n' +
           'San Francisco Giants    |  4\n' +
           'Philadelphia Phillies   |  2',
           'A 1 1 57 1 42 0 C\n' +
           'B 1 2 45 0 32 1 E\n' +
           'C 2 1 57 1 59 3 G\n' +
           'D 2 1 47 3 54 1 G\n' +
           'E 2 2 32 1 51 3 H\n' +
           'F 2 2 56 2 55 3 H\n' +
           'G 3 1 47 0 59 4 I\n' +
           'H 3 2 55 4 51 2 I\n' +
           'I 4 0 55 0 59 0 X\n']

wsinp1 = ['10/20/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|San Francisco 3, Toronto 1>*',
          '10/21/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|San Francisco 8, Toronto 5>*',
          '10/23/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Toronto 6, San Francisco 4>*',
          '10/24/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|San Francisco 8, Toronto 4>*']

wsoutp1 = ['World Series            |  W\n' +
           '------------------------|----\n' +
           'San Francisco Giants    |  3\n' +
           'Toronto Blue Jays       |  1',
           'A 1 1 57 1 42 0 C\n' +
           'B 1 2 45 0 32 1 E\n' +
           'C 2 1 57 1 59 3 G\n' +
           'D 2 1 47 3 54 1 G\n' +
           'E 2 2 32 1 51 3 H\n' +
           'F 2 2 56 2 55 3 H\n' +
           'G 3 1 47 0 59 4 I\n' +
           'H 3 2 55 4 51 2 I\n' +
           'I 4 0 55 3 59 1 X\n']

wsinp2 = ['10/25/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Toronto 3, San Francisco 0>*',
          '10/27/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Toronto 5, San Francisco 3>*',
          '10/28/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
          '*<https://game_box_0.html|Toronto 9, San Francisco 8>*']

wsoutp2 = ['World Series            |  W\n' +
           '------------------------|----\n' +
           'San Francisco Giants    |  3\n' +
           'Toronto Blue Jays       |  4',
           'A 1 1 57 1 42 0 C\n' +
           'B 1 2 45 0 32 1 E\n' +
           'C 2 1 57 1 59 3 G\n' +
           'D 2 1 47 3 54 1 G\n' +
           'E 2 2 32 1 51 3 H\n' +
           'F 2 2 56 2 55 3 H\n' +
           'G 3 1 47 0 59 4 I\n' +
           'H 3 2 55 4 51 2 I\n' +
           'I 4 0 55 3 59 4 X\n']


def test():
  appTest = AppTest(playoffs_in='data/playoffs_in.txt',
                    settings_in='data/settings_playoffs.txt',
                    standings_in='data/standings_final.txt')
  appTest.setup()

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  for i in wcinpt:
    chat_post_message('testing', i)

  time.sleep(2)
  appTest.process_final_scores()
  assert_equals(appTest.process_playoffs(), wcoutpt[0])
  with open(appTest.get_playoffs_out(), 'r') as f:
    assert_equals(f.read(), wcoutpt[1])

  for i in dsinp1:
    chat_post_message('testing', i)

  time.sleep(2)
  appTest.process_final_scores()
  assert_equals(appTest.process_playoffs(), dsoutp1[0])
  with open(appTest.get_playoffs_out(), 'r') as f:
    assert_equals(f.read(), dsoutp1[1])

  for i in dsinp2:
    chat_post_message('testing', i)

  time.sleep(2)
  appTest.process_final_scores()
  assert_equals(appTest.process_playoffs(), dsoutp2[0])
  with open(appTest.get_playoffs_out(), 'r') as f:
    assert_equals(f.read(), dsoutp2[1])

  for i in csinp1:
    chat_post_message('testing', i)

  time.sleep(2)
  appTest.process_final_scores()
  assert_equals(appTest.process_playoffs(), csoutp1[0])
  with open(appTest.get_playoffs_out(), 'r') as f:
    assert_equals(f.read(), csoutp1[1])

  for i in csinp2:
    chat_post_message('testing', i)

  time.sleep(2)
  appTest.process_final_scores()
  assert_equals(appTest.process_playoffs(), csoutp2[0])
  with open(appTest.get_playoffs_out(), 'r') as f:
    assert_equals(f.read(), csoutp2[1])

  for i in wsinp1:
    chat_post_message('testing', i)

  time.sleep(2)
  appTest.process_final_scores()
  assert_equals(appTest.process_playoffs(), wsoutp1[0])
  with open(appTest.get_playoffs_out(), 'r') as f:
    assert_equals(f.read(), wsoutp1[1])

  for i in wsinp2:
    chat_post_message('testing', i)

  time.sleep(2)
  appTest.process_final_scores()
  assert_equals(appTest.process_playoffs(), wsoutp2[0])
  with open(appTest.get_playoffs_out(), 'r') as f:
    assert_equals(f.read(), wsoutp2[1])

  appTest.handle_close()
  t1.join()


if __name__ == '__main__':
  test()
