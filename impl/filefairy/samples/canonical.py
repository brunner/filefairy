#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample data for filefairy.py golden test."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/impl/fairylab/samples', '', _path))

from common.elements.elements import sitelinks  # noqa

subtitle = ''

tmpl = 'home.html'

context = {
    'sitelinks': sitelinks(),
}
