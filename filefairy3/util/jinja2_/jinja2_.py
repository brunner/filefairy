#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jinja2
import os
import re

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/jinja2_', '', _path)


def env():
    ldr = jinja2.FileSystemLoader(os.path.join(_root, 'resource/templates'))
    ext = ['jinja2.ext.do']
    return jinja2.Environment(
        loader=ldr, extensions=ext, trim_blocks=True, lstrip_blocks=True)
