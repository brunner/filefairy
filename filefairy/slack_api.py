#!/usr/bin/env python

import json
import os
import tokens
import urllib
import urllib2


class SlackApi(object):

  def __init__(self, logger):
    self.logger = logger
    self.setChannels()
    self.setUsers()

  def call_(self, method, params):
    url = 'https://slack.com/api/{}'.format(method)
    obj = {'ok': False}

    try:
      request = urllib2.Request(url, urllib.urlencode(params))
      response = urllib2.urlopen(request)
      obj = json.loads(response.read())
    except urllib2.URLError as e:
      if hasattr(e, 'reason'):
        self.logger.log('Failed to reach server. {0}.'.format(e.reason))
      elif hasattr(e, 'code'):
        self.logger.log('Server failed to handle request. {0}.'.format(e.code))
    except:
      self.logger.log('Unspecified exception.')

    return obj

  def chatPostMessage(self, channel, text, attachments=[], thread_ts=''):
    return self.call_('chat.postMessage', {
        'token': tokens.filefairy,
        'channel': channel,
        'text': text,
        'as_user': 'true',
        'attachments': attachments,
        'link_names': 'true',
        'thread_ts': thread_ts
    })

  def chatUpdate(self, ts, channel, text, attachments=[]):
    return self.call_('chat.update', {
        'token': tokens.filefairy,
        'ts': ts,
        'channel': channel,
        'text': text,
        'as_user': 'true',
        'attachments': attachments,
    })

  def reactionsAdd(self, name, channel, timestamp):
    return self.call_('reactions.add', {
        'token': tokens.filefairy,
        'name': name,
        'channel': channel,
        'timestamp': timestamp
    })

  def rtmConnect(self):
    return self.call_('rtm.connect', {'token': tokens.filefairy})

  def channelsList(self):
    return self.call_('channels.list', {'token': tokens.filefairy})

  def groupsList(self):
    return self.call_('groups.list', {'token': tokens.filefairy})

  def usersList(self):
    return self.call_('users.list', {'token': tokens.filefairy})

  def imOpen(self, user):
    return self.call_('im.open', {
        'token': tokens.filefairy,
        'user': user,
        'return_im': 'true'
    })

  def setChannels(self):
    self.channels = {}

    obj = self.channelsList()
    if obj['ok'] and 'channels' in obj:
      for channel in obj['channels']:
        key, value = channel['id'], channel['name']
        self.channels[key] = value

    obj = self.groupsList()
    if obj['ok'] and 'groups' in obj:
      for group in obj['groups']:
        key, value = group['id'], group['name']
        self.channels[key] = value

  def getChannel(self, key):
    if key in self.channels:
      return self.channels[key]

    return ''

  def setUsers(self):
    self.users = {}

    obj = self.usersList()
    if obj['ok'] and 'members' in obj:
      for user in obj['members']:
        key, value = user['id'], user['name']
        self.users[key] = value

  def getUser(self, key):
    if key in self.users:
      return self.users[key]

    return ''

  def filesUpload(self, content, filename, channel):
    return self.call_('files.upload', {
        'token': tokens.filefairy,
        'content': content,
        'filename': filename,
        'channels': channel,
    })


class TestSlackApi(SlackApi):

  def __init__(self, logger):
    self.logger = logger

  def call_(self, method, params):
    self.logger.log('Test mocked {}.'.format(method))
    return {'ok': True}

  def filesUpload(self, path, filename, channel, keep=False):
    params = {'filename': filename, 'channel': channel}
    obj = json.dumps(params, sort_keys=True)
    self.logger.log('Test mocked files.upload.')
    return {'ok': True}

# TODO: Move the below utilities into a helper class.
cities = ['Arizona', 'Atlanta', 'Baltimore', 'Boston', 'Chicago', 'Chicago', 'Cincinnati',
         'Cleveland', 'Colorado', 'Detroit', 'Miami', 'Houston', 'Kansas City', 'Los Angeles',
         'Los Angeles', 'Milwaukee', 'Minnesota', 'New York', 'New York', 'Oakland', 'Philadelphia',
         'Pittsburgh', 'San Diego', 'Seattle', 'San Francisco', 'St. Louis', 'Tampa Bay', 'Texas',
         'Toronto', 'Washington']

abbs = ['ARI', 'ATL', 'BAL', 'BOS', 'CWS', 'CHC', 'CIN', 'CLE', 'COL', 'DET', 'MIA', 'HOU', 'KC',
        'LAA', 'LAD', 'MIL', 'MIN', 'NYY', 'NYM', 'OAK','PHI', 'PIT', 'SD', 'SEA', 'SF', 'STL',
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
