#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/news', '', _path)
sys.path.append(_root)
from util.file_.file_ import recreate  # noqa


def box_scores(then):
    box_here = os.path.join(_root, 'resource/download/news/html/box_scores')
    game_here = os.path.join(_root, 'resource/download/news/txt/leagues')

    box_there = os.path.join(_root, 'resource/extract/box_scores')
    game_there = os.path.join(_root, 'resource/extract/game_logs')
    recreate(box_there)
    recreate(game_there)

    now = then
    for box in os.listdir(box_here):
        box_here_fname = os.path.join(box_here, box)
        if not os.path.isfile(box_here_fname):
            continue
        with open(box_here_fname, 'r', encoding='iso-8859-1') as f:
            box_read = f.read()

        game = box.replace('game_box', 'log').replace('html', 'txt')
        game_here_fname = os.path.join(game_here, game)
        if not os.path.isfile(game_here_fname):
            continue
        with open(game_here_fname, 'r', encoding='iso-8859-1') as f:
            game_read = f.read()

        pattern = 'MLB Box Scores[^\d]+(\d{2}\/\d{2}\/\d{4})'
        match = re.findall(pattern, box_read)
        if not match:
            continue

        date = datetime.datetime.strptime(match[0], '%m/%d/%Y')
        if date < then:
            continue

        box_there_fname = os.path.join(box_there, box)
        with open(box_there_fname, 'w') as f:
            f.write(box_read)

        game_there_fname = os.path.join(game_there, game)
        with open(game_there_fname, 'w') as f:
            f.write(game_read)

        if date >= now:
            now = date + datetime.timedelta(days=1)

    return now
