#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/scripts', '', _path)
sys.path.append(_root)

from common.os_.os_ import chdir  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from impl.filefairy.filefairy import main  # noqa
from tasks.git.git import Git  # noqa

FAIRYLAB_DIR = _root + '/fairylab'
GAMEDAY_DIR = os.path.join(FAIRYLAB_DIR, 'gameday')
NAMES = ['index.html', 'dashboard', 'gameday', 'news', 'sandbox', 'standings']
REMOTE = 'brunnerj@brunnerj.com:/home/brunnerj/public_html/fairylab/'


def check_status():
    return Git.check(['git', 'status']).get_debug()[0].get_extra()['stdout']


def upload_to_fairylab():
    for name in NAMES:
        local = '/home/jbrunner/filefairy/fairylab/' + name
        check_output(['scp', '-r', local, REMOTE])


check_output(['rm', '-rf', GAMEDAY_DIR])
check_output(['mkdir', GAMEDAY_DIR])

main()

stdout = check_status()
if 'impl/sandbox/goldens/canonical.html' in stdout:
    check_output([
        'cp', 'impl/sandbox/goldens/canonical.html',
        '/home/jbrunner/filefairy/fairylab/sandbox/index.html'
    ])

if 'fairylab/' not in stdout:
    print('nothing changed')
else:
    revert = input('revert fairylab? ')
    if revert == 'y':
        check_output(['git', 'checkout', 'fairylab'])

upload = input('upload latest to fairylab? ')
if upload == 'y':
    upload_to_fairylab()
