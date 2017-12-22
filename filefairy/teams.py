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


nicknames = dict(zip(range(31, 61), [
    'Diamondbacks', 'Braves', 'Orioles', 'Red Sox', 'White Sox', 'Cubs', 'Reds', 'Indians',
    'Rockies', 'Tigers', 'Marlins', 'Astros', 'Royals', 'Angels', 'Dodgers', 'Brewers', 'Twins',
    'Yankees', 'Mets', 'Athletics', 'Phillies', 'Pirates', 'Padres', 'Mariners', 'Giants',
    'Cardinals', 'Rays', 'Rangers', 'Blue Jays', 'Nationals']))


def get_nickname(teamid):
  return lookup_(nicknames, teamid, '')
