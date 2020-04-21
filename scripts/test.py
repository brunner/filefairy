#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/scripts', '', _path))

from common.os_.os_ import chdir  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from impl.filefairy.filefairy import main  # noqa
from tasks.git.git import Git  # noqa

CONTAINING_DIR = re.sub(r'/filefairy/scripts', '', _path)
FAIRYLAB_DIR = CONTAINING_DIR + '/fairylab/static'
GAMEDAY_DIR = os.path.join(FAIRYLAB_DIR, 'gameday')
NAMES = ['index.html', 'dashboard', 'gameday', 'news', 'sandbox', 'standings']
REMOTE = 'brunnerj@brunnerj.com:/home/brunnerj/public_html/fairylab/'

check_output(['rm', '-rf', GAMEDAY_DIR])
check_output(['mkdir', GAMEDAY_DIR])

main()

with chdir(FAIRYLAB_DIR):
    stdout = Git.check(['git', 'status']).get_debug()[0].get_extra()['stdout']

    if 'nothing to commit' in stdout:
        print('nothing to commit')
    else:
        upload = input('copy changes to sandbox? ')
        if upload == 'y':
            for name in NAMES:
                local = '/home/jbrunner/fairylab/static/' + name
                check_output(['scp', '-r', local, REMOTE])

        revert = input('revert fairylab changes? ')
        if revert == 'y':
            check_output(['git', 'checkout', '.'])
