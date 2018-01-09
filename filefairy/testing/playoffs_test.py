#!/usr/bin/env python

from app_test import AppTest
from utils import assert_equals

inpt = ['data/playoffs_wild_card.txt',
        'data/playoffs_division_series.txt',
        'data/playoffs_championship_series.txt',
        'data/playoffs_world_series.txt']


outp = ['AL Wild Card            |  W\n' +
        '------------------------|----\n' +
        'Chicago White Sox       |  1\n' +
        'Cleveland Indians       |  0\n\n' +
        'NL Wild Card            |  W\n' +
        '------------------------|----\n' +
        'Los Angeles Dodgers     |  0\n' +
        'Colorado Rockies        |  1',
        'AL Division Series      |  W\n' +
        '------------------------|----\n' +
        'Chicago White Sox       |  1\n' +
        'Minnesota Twins         |  3\n\n' +
        'AL Division Series      |  W\n' +
        '------------------------|----\n' +
        'Seattle Mariners        |  3\n' +
        'Toronto Blue Jays       |  2\n\n' +
        'NL Division Series      |  W\n' +
        '------------------------|----\n' +
        'Colorado Rockies        |  3\n' +
        'Cincinnati Reds         |  2\n\n' +
        'NL Division Series      |  W\n' +
        '------------------------|----\n' +
        'New York Mets           |  3\n' +
        'San Diego Padres        |  1',
        'AL Championship Series  |  W\n' +
        '------------------------|----\n' +
        'Seattle Mariners        |  2\n' +
        'Minnesota Twins         |  4\n\n' +
        'NL Championship Series  |  W\n' +
        '------------------------|----\n' +
        'Colorado Rockies        |  4\n' +
        'New York Mets           |  3',
        'World Series            |  W\n' +
        '------------------------|----\n' +
        'Colorado Rockies        |  4\n' +
        'Minnesota Twins         |  0']


def assert_playoffs(playoffs_in, format):
  appTest = AppTest(playoffs_in=playoffs_in)
  appTest.setup()
  assert_equals(appTest.process_playoffs(), format)
  with open(appTest.get_playoffs_in(), 'r') as fi:
    with open(appTest.get_playoffs_out(), 'r') as fo:
      assert_equals(fi.read(), fo.read())


def test():
  for i, o in zip(inpt, outp):
    assert_playoffs(i, o)

if __name__ == '__main__':
  test()
