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
  assert_teams(31, 'Arizona', ':dbacks:', '')
  assert_teams(32, 'Atlanta', ':braves:', '')
  assert_teams(33, 'Baltimore', ':orioles:', '')
  assert_teams(34, 'Boston', ':redsox:', '')
  assert_teams(35, 'Chicago', ':whitesox:', 'White Sox')
  assert_teams(36, 'Chicago', ':cubbies:', 'Cubs')
  assert_teams(37, 'Cincinnati', ':reds:', '')
  assert_teams(38, 'Cleveland', ':indians:', '')
  assert_teams(39, 'Colorado', ':rox:', '')
  assert_teams(40, 'Detroit', ':crackeyes:', '')
  assert_teams(41, 'Miami', ':marlins:', '')
  assert_teams(42, 'Houston', ':stros:', '')
  assert_teams(43, 'Kansas City', ':monarchs:', '')
  assert_teams(44, 'Los Angeles', ':angels:', 'Angels')
  assert_teams(45, 'Los Angeles', ':dodgers:', 'Dodgers')
  assert_teams(46, 'Milwaukee', ':brewers:', '')
  assert_teams(47, 'Minnesota', ':twincities:', '')
  assert_teams(48, 'New York', ':yankees:', 'Yankees')
  assert_teams(49, 'New York', ':mets:', 'Mets')
  assert_teams(50, 'Oakland', ':athletics:', '')
  assert_teams(51, 'Philadelphia', ':phillies:', '')
  assert_teams(52, 'Pittsburgh', ':pirates:', '')
  assert_teams(53, 'San Diego', ':pads:', '')
  assert_teams(54, 'Seattle', ':mariners:', '')
  assert_teams(55, 'San Francisco', ':giants:', '')
  assert_teams(56, 'St. Louis', ':cardinals:', '')
  assert_teams(57, 'Tampa Bay', ':rays:', '')
  assert_teams(58, 'Texas', ':rangers:', '')
  assert_teams(59, 'Toronto', ':jays:', '')
  assert_teams(60, 'Washington', ':nationals:', '')


if __name__ == '__main__':
  test()
