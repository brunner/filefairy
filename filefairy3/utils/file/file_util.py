#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/utils/file', '', _path)
sys.path.append(_root)
from utils.subprocess.subprocess_util import check_output  # noqa

_file = os.path.join(_root, 'file')
_name = 'orange_and_blue_league_baseball.tar.gz'
_url = 'https://www.orangeandblueleaguebaseball.com/StatsLab/league_file/' + _name


def wget_file():
    check_output(['rm', '-rf', _file])
    check_output(['mkdir', _file])

    cwd = os.getcwd()
    os.chdir(_file)

    check_output(['wget', _url])
    check_output(['tar', '-xzf', _name])
    os.chdir(cwd)
