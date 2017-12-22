#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from teams import get_city, get_emoji, get_nickname
from utils import assert_equals


def assert_teams(teamid, city, emoji, nickname):
  assert_equals(get_city(teamid), city)
  assert_equals(get_emoji(teamid), emoji)
  assert_equals(get_nickname(teamid), nickname)


def test():
  assert_teams(31, 'Arizona', ':dbacks:', 'Diamondbacks')
  assert_teams(32, 'Atlanta', ':braves:', 'Braves')
  assert_teams(33, 'Baltimore', ':orioles:', 'Orioles')
  assert_teams(34, 'Boston', ':redsox:', 'Red Sox')
  assert_teams(35, 'Chicago', ':whitesox:', 'White Sox')
  assert_teams(36, 'Chicago', ':cubbies:', 'Cubs')
  assert_teams(37, 'Cincinnati', ':reds:', 'Reds')
  assert_teams(38, 'Cleveland', ':indians:', 'Indians')
  assert_teams(39, 'Colorado', ':rox:', 'Rockies')
  assert_teams(40, 'Detroit', ':crackeyes:', 'Tigers')
  assert_teams(41, 'Miami', ':marlins:', 'Marlins')
  assert_teams(42, 'Houston', ':stros:', 'Astros')
  assert_teams(43, 'Kansas City', ':monarchs:', 'Royals')
  assert_teams(44, 'Los Angeles', ':angels:', 'Angels')
  assert_teams(45, 'Los Angeles', ':dodgers:', 'Dodgers')
  assert_teams(46, 'Milwaukee', ':brewers:', 'Brewers')
  assert_teams(47, 'Minnesota', ':twincities:', 'Twins')
  assert_teams(48, 'New York', ':yankees:', 'Yankees')
  assert_teams(49, 'New York', ':mets:', 'Mets')
  assert_teams(50, 'Oakland', ':athletics:', 'Athletics')
  assert_teams(51, 'Philadelphia', ':phillies:', 'Phillies')
  assert_teams(52, 'Pittsburgh', ':pirates:', 'Pirates')
  assert_teams(53, 'San Diego', ':pads:', 'Padres')
  assert_teams(54, 'Seattle', ':mariners:', 'Mariners')
  assert_teams(55, 'San Francisco', ':giants:', 'Giants')
  assert_teams(56, 'St. Louis', ':cardinals:', 'Cardinals')
  assert_teams(57, 'Tampa Bay', ':rays:', 'Rays')
  assert_teams(58, 'Texas', ':rangers:', 'Rangers')
  assert_teams(59, 'Toronto', ':jays:', 'Blue Jays')
  assert_teams(60, 'Washington', ':nationals:', 'Nationals')


if __name__ == '__main__':
  test()
