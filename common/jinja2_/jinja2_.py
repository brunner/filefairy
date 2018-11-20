#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jinja2
import os
import re

_path = os.path.dirname(os.path.abspath(__file__))

FILEFAIRY_ROOT = re.sub(r'/common/jinja2_', '', _path)


def env():
    ldr = jinja2.FileSystemLoader(FILEFAIRY_ROOT + '/resource/templates')
    ext = ['jinja2.ext.do']
    return jinja2.Environment(
        loader=ldr, extensions=ext, trim_blocks=True, lstrip_blocks=True)
