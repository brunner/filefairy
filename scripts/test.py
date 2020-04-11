#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/scripts', '', _path))

from impl.filefairy.filefairy import main  # noqa

main()
