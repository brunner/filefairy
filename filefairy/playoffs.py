#!/usr/bin/env python

import os

from teams import get_city, get_nickname


def cast_(s, default):
  return int(s) if s.isdigit() else default


class PlayoffData(object):

  def __init__(self, line=''):
    if line.count(' ') != 7:
      line = '0 0 0 M N 0 0 X'
    
    s, g, l, t0, t1, w0, w1, j = line.split()

    self.s = cast_(s, 0)
    self.g = cast_(g, 0)
    self.l = cast_(l, 0)

    self.t0 = cast_(t0, t0)
    self.t1 = cast_(t1, t1)
    self.w0 = cast_(w0, 0)
    self.w1 = cast_(w1, 0)

    self.j = j

  def __str__(self):
    line = [self.s, self.g, self.l, self.t0, self.t1, self.w0, self.w1, self.j]
    return ' '.join([str(k) for k in line])

  def contains(self, t):
    return self.t0 == t or self.t1 == t

  def decided(self):
    return self.w0 == self.g or self.w1 == self.g

  def enter(self, t, w):
    if self.t0 == t:
      self.w0 = self.w0 + w

    if self.t1 == t:
      self.w1 = self.w1 + w

  def fill(self, i, t):
    if self.t0 == i:
      self.t0 = t

    if self.t1 == i:
      self.t1 = t

  def resolved(self):
    return isinstance(self.t0, int) and isinstance(self.t1, int)

  def started(self):
    return self.w0 + self.w1 > 0


class Playoffs(object):

  def __init__(self, playoffs_in=''):
    self.data = {}
    if playoffs_in:
      self.read(playoffs_in)

  def read(self, playoffs_in):
    """Read playoffs data from file.

    Args:
        playoffs_in: the file to read the playoffs data from.
    Returns:
        None.

    """
    d = {}
    if os.path.isfile(playoffs_in):
      with open(playoffs_in, 'r') as f:
        for line in f.readlines():
          if line.count(' '):
            i, line = line.split(' ', 1)
            d[i] = PlayoffData(line)

    self.data = d

  def write(self, playoffs_out):
    """Write playoffs data to file.

    Args:
        standings_out: the file to write the standings data to.
    Returns:
        None

    """
    d = self.data
    lines = []
    for i in sorted(d.keys()):
      lines.append('{} {}\n'.format(i, d[i]))

    if os.path.isfile(playoffs_out):
      with open(playoffs_out, 'w') as f:
        f.writelines(lines)

  def enter(self, t, w):
    if w <= 0:
      return

    d = self.data
    for i in sorted(d.keys(), reverse=True):
      if d[i].resolved() and d[i].contains(t):
        d[i].enter(t, w)
        if d[i].decided() and d[i].j in d:
          j = d[i].j
          d[j].fill(i, t)
        break

  def format(self):
    """Return a string representation of the playoff tree.

    Args:
        None
    Returns:
        the string representation of the playoff tree.

    """
    d = self.data

    s = 1
    for i in sorted(d.keys(), reverse=True):
      if d[i].started():
        s = max(s, d[i].s)

    keys = filter(lambda i: d[i].s == s, sorted(d.keys()))
    title = ['Wild Card', 'Division Series', 'Championship Series', 'World Series'][s - 1]

    ret = [self.format_internal(d[i], title) for i in keys]
    return '\n\n'.join(ret), ''.join([c for c in title if c.isupper()])

  def format_internal(self, p, title):
    """Populates a playoffs template with data for a series.

    Args:
        p: the playoffs data for the series.
        title: the title of the series (e.g. 'Wild Card')
    Returns:
        the populated playoffs template.

    """
    div = ' | '
    top = '{ktitle:<23}{div} W\n' + \
          '------------------------|----'
    row = '{team:<23}{div}{w:>2}'

    l = ['', 'AL ', 'NL '][p.l]
    lines = [top.format(ktitle=(l + title), div=div)]

    team0 = ' '.join([get_city(p.t0), get_nickname(p.t0)])
    lines.append(row.format(team=team0, div=div, w=p.w0))

    team1 = ' '.join([get_city(p.t1), get_nickname(p.t1)])
    lines.append(row.format(team=team1, div=div, w=p.w1))

    return '\n'.join(lines)
