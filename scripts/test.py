#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/scripts', '', _path))

from common.subprocess_.subprocess_ import check_output  # noqa
from impl.filefairy.filefairy import main  # noqa

CONTAINING_DIR = re.sub(r'/filefairy/scripts', '', _path)
FAIRYLAB_DIR = CONTAINING_DIR + '/fairylab/static'
GAMEDAY_DIR = os.path.join(FAIRYLAB_DIR, 'gameday')

check_output(['rm', '-rf', GAMEDAY_DIR])
check_output(['mkdir', GAMEDAY_DIR])

main()
