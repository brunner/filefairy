#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/news', '', _path)
sys.path.append(_root)
from util.datetime_.datetime_ import datetime_datetime_pst  # noqa
from util.file_.file_ import recreate  # noqa

_box_here = os.path.join(_root, 'resource/download/news/html/box_scores')
_box_there = os.path.join(_root, 'resource/extract/box_scores')
_game_here = os.path.join(_root, 'resource/download/news/txt/leagues')
_game_there = os.path.join(_root, 'resource/extract/game_logs')
_leagues_here = os.path.join(_root, 'resource/download/news/txt/leagues')
_leagues_there = os.path.join(_root, 'resource/extract/leagues')


def extract_box_scores(then):
    recreate(_box_there)
    recreate(_game_there)

    now = then
    for box in os.listdir(_box_here):
        box_here_fname = os.path.join(_box_here, box)
        if not os.path.isfile(box_here_fname):
            continue
        with open(box_here_fname, 'r', encoding='iso-8859-1') as f:
            box_read = f.read()

        game = box.replace('game_box', 'log').replace('html', 'txt')
        game_here_fname = os.path.join(_game_here, game)
        if not os.path.isfile(game_here_fname):
            continue
        with open(game_here_fname, 'r', encoding='iso-8859-1') as f:
            game_read = f.read()

        pattern = 'MLB Box Scores[^\d]+(\d{2}\/\d{2}\/\d{4})'
        match = re.findall(pattern, box_read)
        if not match:
            continue

        d = datetime.datetime.strptime(match[0], '%m/%d/%Y')
        date = datetime_datetime_pst(d.year, d.month, d.day)
        if date < then:
            continue

        box_there_fname = os.path.join(_box_there, box)
        with open(box_there_fname, 'w') as f:
            f.write(box_read)

        game_there_fname = os.path.join(_game_there, game)
        with open(game_there_fname, 'w') as f:
            f.write(game_read)

        if date >= now:
            now = date + datetime.timedelta(days=1)

    return now


def extract_leagues(then):
    recreate(_leagues_there)

    now = then
    for key in ['injuries', 'news', 'transactions']:
        fname = 'league_100_{}.txt'.format(key)
        here_fname = os.path.join(_leagues_here, fname)
        if not os.path.isfile(here_fname):
            continue
        with open(here_fname, 'r', encoding='iso-8859-1') as f:
            read = f.read()

        there_fname = os.path.join(_leagues_there, '{}.txt'.format(key))
        with open(there_fname, 'w') as f:
            match = re.findall('\d{8}\t[^\n]+\n', read.strip() + '\n')
            for m in match:
                d = datetime.datetime.strptime(m[:8], '%Y%m%d')
                date = datetime_datetime_pst(d.year, d.month, d.day)
                if date < then:
                    continue
                elif date > now:
                    now = date
                f.write(m)

    return now
