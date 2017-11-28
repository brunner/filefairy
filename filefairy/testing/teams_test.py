#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from teams import get_city, get_emoji, get_neighbor, get_nickname
from utils import assert_equals


def assert_team(teamid, city, emoji, neighbor, nickname):
  assert_equals(get_city(teamid), city)
  assert_equals(get_emoji(teamid), emoji)
  assert_equals(get_neighbor(teamid), neighbor)
  assert_equals(get_nickname(teamid), nickname)


def test():
  assert_team(31, 'Arizona', ':dbacks:', -1, '')
  assert_team(32, 'Atlanta', ':braves:', -1, '')
  assert_team(33, 'Baltimore', ':orioles:', -1, '')
  assert_team(34, 'Boston', ':redsox:', -1, '')
  assert_team(35, 'Chicago', ':whitesox:', 36, 'White Sox')
  assert_team(36, 'Chicago', ':cubbies:', 35, 'Cubs')
  assert_team(37, 'Cincinnati', ':reds:', -1, '')
  assert_team(38, 'Cleveland', ':indians:', -1, '')
  assert_team(39, 'Colorado', ':rox:', -1, '')
  assert_team(40, 'Detroit', ':crackeyes:', -1, '')
  assert_team(41, 'Miami', ':marlins:', -1, '')
  assert_team(42, 'Houston', ':stros:', -1, '')
  assert_team(43, 'Kansas City', ':monarchs:', -1, '')
  assert_team(44, 'Los Angeles', ':angels:', 45, 'Angels')
  assert_team(45, 'Los Angeles', ':dodgers:', 44, 'Dodgers')
  assert_team(46, 'Milwaukee', ':brewers:', -1, '')
  assert_team(47, 'Minnesota', ':twincities:', -1, '')
  assert_team(48, 'New York', ':yankees:', 49, 'Yankees')
  assert_team(49, 'New York', ':mets:', 48, 'Mets')
  assert_team(50, 'Oakland', ':athletics:', -1, '')
  assert_team(51, 'Philadelphia', ':phillies:', -1, '')
  assert_team(52, 'Pittsburgh', ':pirates:', -1, '')
  assert_team(53, 'San Diego', ':pads:', -1, '')
  assert_team(54, 'Seattle', ':mariners:', -1, '')
  assert_team(55, 'San Francisco', ':giants:', -1, '')
  assert_team(56, 'St. Louis', ':cardinals:', -1, '')
  assert_team(57, 'Tampa Bay', ':rays:', -1, '')
  assert_team(58, 'Texas', ':rangers:', -1, '')
  assert_team(59, 'Toronto', ':jays:', -1, '')
  assert_team(60, 'Washington', ':nationals:', -1, '')


if __name__ == '__main__':
  test()
