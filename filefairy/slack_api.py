#!/usr/bin/env python

import json
import os
import tokens
import urllib
import urllib2


def call_(method, params):
  url = 'https://slack.com/api/{}'.format(method)
  obj = {'ok': False}
  try:
    request = urllib2.Request(url, urllib.urlencode(params))
    response = urllib2.urlopen(request)
    obj = json.loads(response.read())
  except:
    pass
  return obj


def chatPostMessage(channel, text, attachments=[], thread_ts=''):
  return call_('chat.postMessage', {
      'token': tokens.filefairy,
      'channel': channel,
      'text': text,
      'as_user': 'true',
      'attachments': attachments,
      'link_names': 'true',
      'thread_ts': thread_ts
  })


def filesUpload(content, filename, channel):
  return call_('files.upload', {
      'token': tokens.filefairy,
      'content': content,
      'filename': filename,
      'channels': channel,
  })


def rtmConnect():
  return call_('rtm.connect', {'token': tokens.filefairy})


# TODO: Move the below utilities into a helper class.
cities = ['Arizona', 'Atlanta', 'Baltimore', 'Boston', 'Chicago', 'Chicago', 'Cincinnati',
          'Cleveland', 'Colorado', 'Detroit', 'Miami', 'Houston', 'Kansas City', 'Los Angeles',
          'Los Angeles', 'Milwaukee', 'Minnesota', 'New York', 'New York', 'Oakland', 'Philadelphia',
          'Pittsburgh', 'San Diego', 'Seattle', 'San Francisco', 'St. Louis', 'Tampa Bay', 'Texas',
          'Toronto', 'Washington']

abbs = ['ARI', 'ATL', 'BAL', 'BOS', 'CWS', 'CHC', 'CIN', 'CLE', 'COL', 'DET', 'MIA', 'HOU', 'KC',
        'LAA', 'LAD', 'MIL', 'MIN', 'NYY', 'NYM', 'OAK', 'PHI', 'PIT', 'SD', 'SEA', 'SF', 'STL',
        'TB', 'TEX', 'TOR', 'WAS']

nicks = ['White Sox', 'Cubs', 'Angels', 'Dodgers', 'Yankees', 'Mets']


def getNickname(number):
  if number < 31 or number > 60:
    return '???'
  return nicks[number - 31]


emoji = [':dbacks:', ':braves:', ':orioles:', ':redsox:', ':whitesox:', ':cubbies:', ':reds:',
         ':indians:', ':rox:', ':crackeyes:', ':marlins:', ':stros:', ':monarchs:', ':angels:',
         ':dodgers:', ':brewers:', ':twincities:', ':yankees:', ':mets:', ':athletics:',
         ':phillies:', ':pirates:', ':pads:', ':mariners:', ':giants:', ':cardinals:', ':rays:',
         ':rangers:', ':jays:', ':nationals:']


def getEmoji(number):
  if number < 31 or number > 60:
    return ':grey_question:'
  return emoji[number - 31]


nicksToTeamids = dict(zip(nicks, range(31, 61)))
teamidsToAbbs = dict(zip(range(31, 61), abbs))
teamidsToEmoji = dict(zip(range(31, 61), emoji))
teamidsToCities = dict(zip(range(31, 61), cities))
teamidsToNicks = dict(zip([35, 36, 44, 45, 48, 49], nicks))
teamidsToNeighbors = dict(zip([35, 36, 44, 45, 48, 49], [36, 35, 45, 44, 49, 48]))
abbsToEmoji = dict(zip(abbs, emoji))
