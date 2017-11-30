#!/usr/bin/env python


def lookup_(collection, teamid, default):
  return collection[teamid] if teamid in collection else default


cities = dict(zip(range(31, 61), [
    'Arizona', 'Atlanta', 'Baltimore', 'Boston', 'Chicago', 'Chicago', 'Cincinnati',
    'Cleveland', 'Colorado', 'Detroit', 'Miami', 'Houston', 'Kansas City', 'Los Angeles',
    'Los Angeles', 'Milwaukee', 'Minnesota', 'New York', 'New York', 'Oakland', 'Philadelphia',
    'Pittsburgh', 'San Diego', 'Seattle', 'San Francisco', 'St. Louis', 'Tampa Bay', 'Texas',
    'Toronto', 'Washington']))


def get_city(teamid):
  return lookup_(cities, teamid, '')


emoji = dict(zip(range(31, 61), [
    ':dbacks:', ':braves:', ':orioles:', ':redsox:', ':whitesox:', ':cubbies:', ':reds:',
    ':indians:', ':rox:', ':crackeyes:', ':marlins:', ':stros:', ':monarchs:', ':angels:',
    ':dodgers:', ':brewers:', ':twincities:', ':yankees:', ':mets:', ':athletics:',
    ':phillies:', ':pirates:', ':pads:', ':mariners:', ':giants:', ':cardinals:', ':rays:',
    ':rangers:', ':jays:', ':nationals:']))


def get_emoji(teamid):
  return lookup_(emoji, teamid, '')


nicknames = dict(zip([35, 36, 44, 45, 48, 49], [
    'White Sox', 'Cubs', 'Angels', 'Dodgers', 'Yankees', 'Mets']))


def get_nickname(teamid):
  return lookup_(nicknames, teamid, '')
