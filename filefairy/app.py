#!/usr/bin/env python

import copy
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib2
import websocket

from slack_api import chat_post_message, files_upload, rtm_connect
from teams import get_city, get_emoji, get_nickname

import logging
logging.basicConfig()


class Standings(object):

  def __init__(self):
    self.w = {'s': 0, 'w': 0}
    self.l = {'s': 0, 'w': 0}

    self.gb = {'d': 0, 'w': 0}
    self.mn = {'d': [], 'w': []}
    self.tn = {'d': [], 'w': []}

    self.d0 = False
    self.games = []
    self.p = ''


class App(object):

  def __init__(self):
    self.file_url = 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'
    self.lock = threading.Lock()
    self.playoffs_in = 'data/playoffs.txt'
    self.settings_in = 'data/settings.txt'
    self.standings_in = 'data/standings.txt'
    self.ws = None

  def setup(self):
    self.file_date = self.get_file_date(self.get_page(self.file_url))
    self.final_scores = []
    self.injuries = []
    self.live_tables = []
    self.tick = 0
    self.playoffs = self.read_playoffs(self.get_playoffs_in())
    self.playoffs_completed = False
    self.settings = self.read_settings(self.get_settings_in())
    self.standings = self.read_standings(self.get_standings_in())
    self.keep_running = True

  def get_path(self):
    return os.path.expanduser('~') + '/orangeandblueleague/filefairy/'

  def get_playoffs_in(self):
    p_i = self.playoffs_in
    if os.path.isfile(self.get_path() + 'data/playoffs_over.txt'):
      p_i = 'data/playoffs_over.txt'
    return self.get_path() + p_i if p_i else ''

  def get_playoffs_out(self):
    return self.get_path() + 'data/playoffs.txt'

  def get_settings_in(self):
    s_i = self.settings_in
    if os.path.isfile(self.get_path() + 'data/settings_over.txt'):
      s_i = 'data/settings_over.txt'
    return self.get_path() + s_i if s_i else ''

  def get_standings_in(self):
    s_i = self.standings_in
    if os.path.isfile(self.get_path() + 'data/standings_over.txt'):
      s_i = 'data/standings_over.txt'
    return self.get_path() + s_i if s_i else ''

  def get_standings_out(self):
    return self.get_path() + 'data/standings.txt'

  def get_general_name(self):
    return 'general'

  def get_live_sim_discussion_name(self):
    return 'live-sim-discussion'

  def get_testing_name(self):
    return 'testing'

  def get_statsplus_id(self):
    return 'C7JSGHW8G'

  def get_testing_id(self):
    return 'G3SUFLMK4'

  def get_sleep(self):
    return 120

  def get_page(self, url):
    try:
      return urllib2.urlopen(url).read()
    except:
      return ''

  def read_playoffs(self, playoffs_in):
    """Read playoffs data from file.

    Args:
        playoffs_in: the file to read the playoffs data from.
    Returns:
        a tree of playoff series with current win totals.

    """
    p = {}
    if os.path.isfile(playoffs_in):
      with open(playoffs_in, 'r') as f:
        for line in f.readlines():
          i, s, l, t0, w0, t1, w1, j = line.split()
          p[i] = {
              's': int(s),
              'l': int(l),
              't0': int(t0) if t0.isdigit() else t0,
              'w0': int(w0),
              't1': int(t1) if t1.isdigit() else t1,
              'w1': int(w1),
              'j': j,
          }
    return p

  def write_playoffs(self, playoffs_out, p):
    """Write playoffs data to file.

    Args:
        standings_out: the file to write the standings data to.
        s: the copy of the standings data.
    Returns:
        None

    """
    lines = []
    for i in sorted(p.keys()):
      k = ['s', 'l', 't0', 'w0', 't1', 'w1', 'j']
      lines.append(' '.join([i] + [str(p[i][j]) for j in k]) + '\n')
    if os.path.isfile(playoffs_out):
      with open(playoffs_out, 'w') as f:
        f.writelines(lines)

  def read_settings(self, settings_in):
    """Read settings data from file.

    Args:
        settings_in: the file to read the settings data from.
    Returns:
        an object containing the settings data.

    """
    s = {}
    if os.path.isfile(settings_in):
      with open(settings_in, 'r') as f:
        s = json.loads(f.read())
    return s


  def read_standings(self, standings_in):
    """Read standings data from file.

    Args:
        standings_in: the file to read the standings data from.
    Returns:
        a mapping of team ids to season win/loss pairs.

    """
    s = {t: Standings() for t in range(31, 61)}
    if os.path.isfile(standings_in):
      with open(standings_in, 'r') as f:
        for line in f.readlines():
          t, w, l = [int(n) for n in line.split()]
          s[t].w['s'], s[t].l['s'] = w, l
    return s

  def write_standings(self, standings_out, s):
    """Write standings data to file.

    Args:
        standings_out: the file to write the standings data to.
        s: the copy of the standings data.
    Returns:
        None

    """
    lines = ['{} {} {}\n'.format(t, s[t].w['s'], s[t].l['s']) for t in s]
    if os.path.isfile(standings_out):
      with open(standings_out, 'w') as f:
        f.writelines(lines)

  def listen(self):
    def on_message_(ws, message):
      self.lock.acquire()
      obj = json.loads(message)
      if all(k in obj for k in ['type', 'channel', 'text']) and obj['type'] == 'message':
        if obj['channel'] == self.get_statsplus_id():
          self.handle_statsplus(obj['text'])
        if obj['channel'] == self.get_testing_id():
          self.handle_testing(obj['text'])
      self.lock.release()

    obj = rtm_connect()
    if obj['ok'] and 'url' in obj:
      chat_post_message('testing', 'Started listening.')
      self.ws = websocket.WebSocketApp(obj['url'], on_message=on_message_)

      t = threading.Thread(target=self.ws.run_forever)
      t.daemon = True
      t.start()

  def handle_statsplus(self, text):
    if 'MAJOR LEAGUE BASEBALL Final Scores' in text:
      self.handle_final_scores(text)
    elif 'MAJOR LEAGUE BASEBALL Live Table' in text:
      self.handle_live_table(text)
    elif re.findall(r'\d{2}\/\d{2}\/\d{4}', text) and 'was injured' in text:
      self.handle_injuries(text)

  def handle_testing(self, text):
    if text == 'Run git pull.':
      deb = subprocess.check_output(['git', 'pull'])
      chat_post_message(self.get_testing_name(), deb.strip('\n'))
    if text == 'Run git reset.':
      deb = subprocess.check_output(['git', 'reset', '--hard'])
      chat_post_message(self.get_testing_name(), deb.strip('\n'))
    elif text == 'Run setup.':
      self.setup()
      deb, txt = self.format_playoffs()
      files_upload(deb, txt, self.get_testing_name())
      files_upload(self.format_standings_al(), 'AL.txt', self.get_testing_name())
      files_upload(self.format_standings_nl(), 'NL.txt', self.get_testing_name())
      deb = ', '.join(['{}: {}'.format(k.title(), self.settings[k]) for k in self.settings]) + '.'
      chat_post_message(self.get_testing_name(), deb)
    if text == 'Run shutdown.':
      self.keep_running = False

  def handle_final_scores(self, text):
    text = re.sub(r'( MAJOR LEAGUE BASEBALL Final Scores|\*)', '', text)
    if text not in self.final_scores:
      self.final_scores.append(text)
      self.live_tables.append('')
      self.tick = int(time.time())

  def process_final_scores(self):
    for i, finalScore in enumerate(self.final_scores):
      chat_post_message(self.get_live_sim_discussion_name(), finalScore)
      if len(self.final_scores) == len(self.live_tables):
        liveTable = self.live_tables[i]
        for t in range(31, 61):
          if t in [35, 36, 44, 45, 48, 49]:
            continue
          city = get_city(t)
          cw = len(re.findall(r'\|' + re.escape(city), finalScore))
          cl = len(re.findall(r', ' + re.escape(city), finalScore))
          self.add_score(t, cw, cl)

        for t, u in zip([35, 44, 48], [36, 45, 49]):
          city = get_city(t)
          cw = len(re.findall(r'\|' + re.escape(city), finalScore))
          cl = len(re.findall(r', ' + re.escape(city), finalScore))

          ws = re.findall(r'\|' + re.escape(city) + '\s\d+,\s([^\d]+)\d', finalScore)
          ls = re.findall(r'\|([^\d]+)\d+,\s' + re.escape(city), finalScore)

          tn = get_nickname(t)
          tt = re.findall(re.escape(tn) + r'\s+(\d+)', liveTable)
          ts = self.standings[t].w['s']

          un = get_nickname(u)
          ut = re.findall(re.escape(un) + r'\s+(\d+)', liveTable)
          us = self.standings[u].w['s']

          # Hack for 2021 playoffs. Clean up during offseason.
          if self.settings.get('playoffs', False):
            if t == 35:
              self.add_score(t, cw, cl)
            elif u == 45:
              self.add_score(u, cw, cl)
            elif u == 49:
              self.add_score(u, cw, cl)
          elif tt and ut:
            ct = cw + cl
            tw, uw = int(tt[0]) - ts, int(ut[0]) - us
            if ct != 3:
              tl, ul = ct / 2 - tw, ct / 2 - uw
              self.add_score(t, tw, tl)
              self.add_score(u, uw, ul)
            else:
              tl, ul = 0 if tw else 1, 0 if uw else 1
              self.add_score(t, tw, tl)
              self.add_score(u, uw, ul)
            if tw == uw or cw == 1 and cl == 2:
              _ = list(set().union(ws, ls))
              tk, uk = _ if len(_) == 2 else ('', '')
              if ct != 3:
                self.add_game(t, {tk: False, uk: False})
                self.add_game(u, {tk: False, uk: False})
              else:
                td = ws.count(tk) + ls.count(tk) == 2
                ud = ws.count(uk) + ls.count(uk) == 2
                self.add_game(t, {tk: td, uk: ud})
                self.add_game(u, {tk: td, uk: ud})
            else:
              tk, uk = '', ''
              for k in ws:
                tk = k if ws.count(k) == tw and not tk else tk
                uk = k if ws.count(k) == uw and not uk else uk
              for k in ls:
                tk = k if ls.count(k) == tl and not tk else tk
                uk = k if ls.count(k) == ul and not uk else uk
              self.add_game(t, {tk: False})
              self.add_game(u, {uk: False})
          else:
            _ = list(set().union(ws, ls))
            sk = _[0] if len(_) == 1 else ''
            if tt:
              self.add_score(t, cw, cl)
              self.add_game(t, {sk: False})
              self.add_game(u, {'': False})
            if ut:
              self.add_score(u, cw, cl)
              self.add_game(t, {'': False})
              self.add_game(u, {sk: False})

    for t, u in zip([35, 44, 48], [36, 45, 49]):
      if not len(self.standings[t].games):
        continue
      tgames, ugames = self.standings[t].games, self.standings[u].games
      if len(tgames) < 2:
        continue
      for i in range(len(tgames)):
        if len(tgames[i].keys()) == 2:
          vk, wk = tgames[i].keys()
          tvn, uvn, twn, uwn = 0, 0, 0, 0
          for j in tgames[i - 1::-1]:
            if vk not in j and wk not in j:
              break
            if vk in j:
              tvn += 1
            if wk in j:
              twn += 1
          for j in ugames[i - 1::-1]:
            if vk not in j and wk not in j:
              break
            if vk in j:
              uvn += 1
            if wk in j:
              uwn += 1
          for j in tgames[i + 1:]:
            if vk not in j and wk not in j:
              break
            if vk in j:
              tvn += 1
            if wk in j:
              twn += 1
          for j in ugames[i + 1:]:
            if vk not in j and wk not in j:
              break
            if vk in j:
              uvn += 1
            if wk in j:
              uwn += 1
          if tvn > twn:
            if tgames[i][vk]:
              self.add_score(t, 0, 1)
              tgames[i][vk] = False
              ugames[i][vk] = False
            elif ugames[i][wk]:
              self.add_score(u, 0, 1)
              tgames[i][wk] = False
              ugames[i][wk] = False
          elif twn > tvn:
            if tgames[i][wk]:
              self.add_score(t, 0, 1)
              tgames[i][wk] = False
              ugames[i][wk] = False
            elif ugames[i][vk]:
              self.add_score(u, 0, 1)
              tgames[i][vk] = False
              ugames[i][vk] = False
          elif uvn > uwn:
            if ugames[i][vk]:
              self.add_score(u, 0, 1)
              tgames[i][vk] = False
              ugames[i][vk] = False
            elif tgames[i][wk]:
              self.add_score(t, 0, 1)
              tgames[i][wk] = False
              ugames[i][wk] = False
          elif uwn > uvn:
            if ugames[i][wk]:
              self.add_score(u, 0, 1)
              tgames[i][wk] = False
              ugames[i][wk] = False
            elif tgames[i][vk]:
              self.add_score(t, 0, 1)
              tgames[i][vk] = False
              ugames[i][vk] = False

    ret = '\n'.join(self.final_scores)
    self.final_scores, self.live_tables = [], []
    return ret

  def add_score(self, t, w, l):
    if self.settings.get('playoffs', False):
      p = self.playoffs
      if w > 0:
        for k in sorted(p.keys(), reverse=True):
          t0, w0 = p[k]['t0'], p[k]['w0']
          t1, w1 = p[k]['t1'], p[k]['w1']
          if isinstance(t0, int) and isinstance(t1, int) and (t0 == t or t1 == t):
            s = p[k]['s']
            g = [1, 3, 4, 4][s-1]
            if t0 == t:
              p[k]['w0'] = w0 + w
            if t1 == t:
              p[k]['w1'] = w1 + w
            if (t0 == t and w0 + w == g) or (t1 == t and w1 + w == g):
              j = p[k]['j']
              if j == 'X':
                self.playoffs_completed = True
              else:
                if p[j]['t0'] == k:
                  p[j]['t0'] = t
                if p[j]['t1'] == k:
                  p[j]['t1'] = t
                t0, t1 = p[j]['t0'], p[j]['t1']
                if isinstance(t0, int) and isinstance(t1, int):
                  t1, t0 = self.get_ordered(self.standings, [t0, t1], 's')
                p[j]['t0'] = t0
                p[j]['t1'] = t1
            break

    if self.settings.get('standings', False):
      s = self.standings
      s[t].w['s'] += w
      s[t].w['w'] += w
      s[t].l['s'] += l
      s[t].l['w'] += l

  def add_game(self, t, g):
    self.standings[t].games.append(g)

  def handle_live_table(self, text):
    i = len(self.live_tables) - 1
    self.live_tables[i] = text
    self.tick = int(time.time())

  def handle_injuries(self, text):
    if text not in self.injuries:
      self.injuries.append(text)
      self.tick = int(time.time())

  def process_injuries(self):
    lines = []
    if self.injuries:
      lines.append('Injuries:')
      for injury in self.injuries:
        for chunk in injury.split('. '):
          match = re.findall(r'(\<[^\(]+)\(', chunk)
          if match:
            line = re.sub(r'was injured (?:(?:in a|on a|while) )?',
                          '(', match[0].strip())
            if not line == match[0]:
              line += ')'
            lines.append(line)

      self.injuries = []

    ret = '\n'.join(lines)
    if ret:
      chat_post_message(self.get_live_sim_discussion_name(), ret)

    return ret

  def process_records(self):
    ret = self.format_records()
    chat_post_message(self.get_live_sim_discussion_name(), ret)
    return ret

  def process_playoffs(self):
    ret, txt = self.format_playoffs()
    files_upload(ret, txt, self.get_live_sim_discussion_name())
    self.write_playoffs(self.get_playoffs_out(), self.playoffs)
    return ret

  def process_standings(self):
    retA = self.format_standings_al()
    retB = self.format_standings_nl()
    files_upload(retA, 'AL.txt', self.get_live_sim_discussion_name())
    files_upload(retB, 'NL.txt', self.get_live_sim_discussion_name())
    self.write_standings(self.get_standings_out(), self.standings)
    return '\n'.join([retA, retB])

  def handle_close(self):
    self.lock.acquire()
    if self.ws:
      self.ws.close()
      chat_post_message('testing', 'Done listening.')
    self.lock.release()

  def watch(self):
    chat_post_message('testing', 'Started watching.')
    sleep = self.get_sleep()
    while self.keep_running:
      time.sleep(sleep)
      self.lock.acquire()
      self.update_league_file()
      if self.final_scores and int(time.time()) - self.tick > sleep:
        self.process_final_scores()
        self.process_injuries()
        if self.settings.get('standings', False):
          self.process_records()
          self.process_standings()
        if self.settings.get('playoffs', False):
          self.process_playoffs()
      self.lock.release()
    chat_post_message('testing', 'Done watching.')
    self.handle_close()

  def update_league_file(self):
    date = self.get_file_date(self.get_page(self.file_url))
    if date and date != self.file_date:
      chat_post_message(self.get_general_name(), 'File is up.')
      self.file_date = date
      return True
    return False

  def get_file_date(self, page):
    match = re.findall(r'League File Updated: ([^<]+)<', page)
    return match[0] if len(match) else ''

  def format_records(self):
    groups = [
        ('AL East', [33, 34, 48, 57, 59]),
        ('AL Central', [35, 38, 40, 43, 47]),
        ('AL West', [42, 44, 50, 54, 58]),
        ('NL East', [32, 41, 49, 51, 60]),
        ('NL Central', [36, 37, 46, 52, 56]),
        ('NL West', [31, 39, 45, 53, 55]),
    ]
    lines = []
    for group in groups:
      s = self.standings
      ordered = self.get_ordered(s, group[1], 'w')
      formatted = []
      for t in ordered:
        if s[t].w['w'] + s[t].l['w'] > 0:
          emoji = get_emoji(t)
          formatted.append('{0} {1}-{2}'.format(emoji, s[t].w['w'], s[t].l['w']))
      if formatted:
        lines.append('{0}\n{1}'.format(group[0], ' :separator: '.join(formatted)))

    unhandled = []
    for t in [35, 44, 48]:
      if not len(self.standings[t].games):
        continue
      city = get_city(t)
      tgames = self.standings[t].games
      for g in tgames:
        for tk in g:
          if g[tk]:
            unhandled.append('Unhandled loss for {}.'.format(city))
    if unhandled:
      lines.append('_{}_'.format(' '.join(unhandled)))

    return '\n\n'.join(lines)

  def get_standings_keys(self, k):
    return [k + ey for ey in ['gb', 'en', 'mn']]

  def get_games_behind(self, s, u, t0, k):
    """Return the number of games that u is behind t.

    Args:
        s: the copy of the standings data.
        u: the trailing team.
        t0: the leading team.
        k: the key prefix to use when getting standings data ('s' for season, 'w' for week).
    Returns:
        the number of games that u is behind t.

    """
    return (s[u].w[k] - s[t0].w[k] + s[t0].l[k] - s[u].l[k]) / 2.0

  def get_elimination_number(self, s, u, t):
    """Return the elimination number for a team.

    Args:
        s: the copy of the standings data.
        u: the trailing team.
        t0: the leading team.
    Returns:
        the elimination number for u.

    """
    return max(163 - s[t].w['s'] - s[u].l['s'], 0)

  def get_ordered(self, s, group, k):
    """Return a set of teams, sorted by winning percentage.

    Args:
        s: the copy of the standings data.
        group: the set of team ids to sort.
        k: the key prefix to use when getting standings data ('s' for season, 'w' for week).
    Returns:
        the sorted group.

    """
    pct = lambda t: (abs(min([self.get_games_behind(s, u, t, k) for u in group])),
                     float(s[t].w[k]) / ((s[t].w[k] + s[t].l[k]) or 1),
                     s[t].w[k],
                     float(1) / s[t].l[k] if s[t].l[k] else 2,
                     float(1) / t)
    return sorted(group, key=pct, reverse=True)

  def process_elimination_numbers(self, s, ordered, i, k):
    """Annotates the standings with elimination number data.

    Args:
        s: the copy of the standings data.
        ordered: the ordered set of team ids to annotate (e.g. a division).
        i: the index of the team occupying the final playoff spot in ordered.
        k: the key prefix to use when setting annotations ('d' for division, 'w' for wild card).

    """
    kgb, ken, kmn = self.get_standings_keys(k)
    ts = filter(lambda v: s[v].gb[k] >= 0, ordered)
    if len(ts) == len(ordered):
      for t in ordered:
        u0 = sorted(filter(lambda v: v != t, ts), key=lambda v: s[v].l, reverse=True)[0]
        en = self.get_elimination_number(s, u0, t)
        if s[t].mn[k] == [] or en > s[t].mn[k]:
          s[t].mn[k] = en
    else:
      for t in ts:
        for j, u in enumerate(ordered):
          if u == t:
            continue
          if s[u].d0 and (u not in ts or j > i):
            continue
          en = self.get_elimination_number(s, u, t)
          s[u].tn[k].append(en)
          s[t].mn[k].append(en)
      for v in ordered:
        if s[v].mn[k]:
          s[v].mn[k] = sorted(s[v].mn[k], reverse=True)[i]
        elif s[v].tn[k]:
          s[v].tn[k] = sorted(s[v].tn[k])[i]
        if s[v].mn[k] and s[v].tn[k]:
          s[v].tn[k] = []

  def get_playoffs_output(self, pvalue, title):
    """Populates a playoffs template with data for a series.

    Args:
        pvalue: the playoffs data for the series.
        title: the title of the series (e.g. 'Wild Card')
    Returns:
        the populated playoffs template.

    """
    div = ' | '
    top = '{ktitle:<23}{div} W\n' + \
          '------------------------|----'
    row = '{team:<23}{div}{w:>2}'

    k = 'AL ' if pvalue['l'] == 1 else 'NL ' if pvalue['l'] == 2 else ''
    lines = [top.format(ktitle=(k + title), div=div)]

    t0, w0 = pvalue['t0'], pvalue['w0']
    team = ' '.join([get_city(t0), get_nickname(t0)])
    lines.append(row.format(team=team, div=div, w=w0))
    t1, w1 = pvalue['t1'], pvalue['w1']
    team = ' '.join([get_city(t1), get_nickname(t1)])
    lines.append(row.format(team=team, div=div, w=w1))

    return '\n'.join(lines)

  def format_playoffs(self):
    """Return a string representation of the playoff tree for a league.

    Args:
        None
    Returns:
        the string representation of the playoff tree.

    """
    p = self.playoffs

    s = 1
    for k in sorted(p.keys(), reverse=True):
      t0, w0 = p[k]['t0'], p[k]['w0']
      t1, w1 = p[k]['t1'], p[k]['w1']
      if w0 + w1 > 0:
        s = max(s, p[k]['s'])

    keys = filter(lambda k: p[k]['s'] == s, sorted(p.keys()))
    title = 'Wild Card' if s == 1 else \
            'Division Series' if s == 2 else \
            'Championship Series' if s == 3 else \
            'World Series' if s == 4 else ''

    ret = [self.get_playoffs_output(p[k], title) for k in keys]
    return '\n\n'.join(ret), ''.join([c for c in title if c.isupper()])

  def get_standings_output(self, s, kgroup, group, k):
    """Populates a standings template with data for a set of teams.

    Args:
        s: the copy of the standings data.
        kgroup: the title of the group (e.g. 'AL East')
        group: the set of team ids in the group.
        k: the key prefix to use when getting annotations ('d' for division, 'w' for wild card).
    Returns:
        the populated standings template.

    """
    kgb, ken, kmn = self.get_standings_keys(k)
    div = ' | '
    top = '{title:<15}{div}  W{div}  L{div}   GB{div} M#\n' + \
          '----------------|-----|-----|-------|-----'
    row = '{city:<15}{div}{w:>3}{div}{l:>3}{div}{gb:>5}{div}{mn:>3}'

    lines = [top.format(title=kgroup, div=div)]
    for v in self.get_ordered(s, group, 's'):
      city = get_city(v)
      if s[v].p:
        city = s[v].p + city
      w, l, dgb = s[v].w['s'], s[v].l['s'], s[v].gb[k]
      gb = '{:0.1f}'.format(abs(dgb)) if dgb < 0 else '+{:0.1f}'.format(dgb) if dgb > 0 else '-'
      mn = 'X' if s[v].mn[k] == 0 else '' if not s[v].mn[k] else s[v].mn[k]
      lines.append(row.format(city=city, div=div, w=w, l=l, gb=gb, mn=mn))

    return '\n'.join(lines)

  def format_standings_internal(self, east, cent, west, k):
    """Return a string representation of the standings table for a league.

    Args:
        east: the set of team ids in the east division.
        cent: the set of team ids in the central division.
        west: the set of team ids in the west division.
        kgroup: the title of the group (e.g. 'AL East').
        k: the league title prefix (e.g. 'AL').
    Returns:
        the string representation of the standings table.

    """
    s = copy.deepcopy(self.standings)
    keast, kcent, kwest, kwc = [k + ' ' + ey for ey in ['East', 'Central', 'West', 'Wild Card']]

    # Set the games behind and elimination numbers for each division.
    # If a team is the only leader in its division, annotate it with 'dbg0'.
    for group in [east, cent, west]:
      ordered = self.get_ordered(s, group, 's')
      t0, s[t0].gb['d'], s[t0].d0 = ordered[0], 0.0, True
      for u in ordered[1:]:
        gb = self.get_games_behind(s, u, t0, 's')
        s[u].gb['d'] = gb
        if gb == 0.0 and s[t0].d0:
          s[t0].d0 = False
      self.process_elimination_numbers(s, ordered, 0, 'd')

    # Filter division leaders out of the set of wild card teams.
    lg = east + cent + west
    wc = filter(lambda v: s[v].d0 == False, lg)

    # Find the index of the team occupying the final playoff spot in the league.
    ordered = self.get_ordered(s, lg, 's')
    k, j = 0, 2
    for i, t0 in enumerate(ordered):
      if not s[t0].d0:
        k += 1
        if s[t0].gb['d'] == 0:
          j = 3
      if k == j:
        break

    # Set the games behind and elimination numbers for the wild card.
    s[t0].gb['w'] = 0.0
    for v in ordered:
      s[v].gb['w'] = self.get_games_behind(s, v, t0, 's')
    self.process_elimination_numbers(s, ordered, i, 'w')

    # Annotate the standings with team prefixes, if applicable.
    for v in ordered:
      if s[v].tn['d'] == 0 and s[v].tn['w'] == 0:
        # v has been eliminated.
        s[v].p = 'e-'
      if s[v].mn['d'] == 0:
        # v has clinched the division.
        s[v].p = 'x-'
      elif s[v].mn['w'] == 0:
        # v has clinched the wild card.
        s[v].p = 'z-'

    # Feed the annotated standings data into a helper method to populate the standings template.
    groups = zip([keast, kcent, kwest, kwc], [east, cent, west, wc], ['d', 'd', 'd', 'w'])
    ret = [self.get_standings_output(s, kgroup, group, k) for (kgroup, group, k) in groups]
    return '\n\n'.join(ret)

  def format_standings_al(self):
    aleast, alcent, alwest = [33, 34, 48, 57, 59], [35, 38, 40, 43, 47], [42, 44, 50, 54, 58]
    return self.format_standings_internal(aleast, alcent, alwest, 'AL')

  def format_standings_nl(self):
    nleast, nlcent, nlwest = [32, 41, 49, 51, 60], [36, 37, 46, 52, 56], [31, 39, 45, 53, 55]
    return self.format_standings_internal(nleast, nlcent, nlwest, 'NL')


if __name__ == '__main__':
  app = App()
  app.setup()
  app.listen()
  app.watch()
