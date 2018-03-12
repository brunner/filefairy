#!/usr/bin/env python

import jinja2
import os
import re

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/utils/jinja2', '', _path)


def env():
    ldr = jinja2.FileSystemLoader(os.path.join(_root, 'templates'))
    return jinja2.Environment(loader=ldr, trim_blocks=True, lstrip_blocks=True)
