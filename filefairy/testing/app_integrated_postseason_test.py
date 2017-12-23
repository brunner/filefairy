#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from slack_api import chat_post_message
from utils import assert_equals


inpt = ['10/01/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Tampa Bay 9, Houston 6>*',
        '10/02/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Atlanta 5, Los Angeles 3>*',
        'X',
        '10/03/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
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
        '*<https://game_box_0.html|Tampa Bay 9, Toronto 5>*',
        'X',
        '10/07/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Philadelphia 7, Atlanta 2>*\n' +
        '*<https://game_box_0.html|Minnesota 8, Seattle 2>*\n' +
        '*<https://game_box_0.html|San Francisco 3, St. Louis 0>*\n' +
        '*<https://game_box_0.html|Toronto 7, Tampa Bay 6>*',
        '10/08/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Philadelphia 4, Atlanta 3>*\n' +
        '*<https://game_box_0.html|St. Louis 10, San Francisco 5>*',
        '10/10/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|San Francisco 1, St. Louis 0>*',
        'X',
        '10/11/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Toronto 4, Minnesota 2>*',
        '10/12/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Philadelphia 4, San Francisco 1>*\n' +
        '*<https://game_box_0.html|Toronto 8, Minnesota 3>*',
        '10/13/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|San Francisco 5, Philadelphia 4>*',
        '10/14/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Toronto 6, Minnesota 3>*',
        '10/15/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Toronto 7, Minnesota 5>*\n' +
        '*<https://game_box_0.html|San Francisco 4, Philadelphia 3>*',
        'X',
        '10/16/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Philadelphia 6, San Francisco 1>*',
        '10/17/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|San Francisco 8, Philadelphia 4>*',
        '10/19/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|San Francisco 8, Philadelphia 2>*',
        'X',
        '10/20/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|San Francisco 3, Toronto 1>*',
        '10/21/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|San Francisco 8, Toronto 5>*',
        '10/23/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Toronto 6, San Francisco 4>*',
        '10/24/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|San Francisco 8, Toronto 4>*',
        'X',
        '10/25/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Toronto 3, San Francisco 0>*',
        '10/27/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Toronto 5, San Francisco 3>*',
        '10/28/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_0.html|Toronto 9, San Francisco 8>*',
        'X']

exps = ['data/exports1.html',
        'data/exports2.html',
        'data/exports3.html',
        'data/exports4.html',
        'data/exports5.html',
        'data/exports6.html',
        'data/exports7.html',
        'data/exports8.html']


def test():
  appTest = AppTest(file_url=exps.pop(),
                    playoffs_in='data/playoffs_in.txt',
                    settings_in='data/settings_playoffs.txt',
                    standings_in='data/standings_final.txt')
  appTest.setup()

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  t2 = threading.Thread(target=appTest.watch)
  t2.start()
  time.sleep(2)

  for i in inpt:
    if i == 'X':
      time.sleep(12)
      appTest.file_url = exps.pop()
    else:
      time.sleep(1)
      chat_post_message('testing', i)

  time.sleep(1)
  chat_post_message('testing', 'Run app shutdown.')

  t1.join()
  t2.join()


if __name__ == '__main__':
  test()
