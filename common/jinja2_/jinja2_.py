#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for jinja2 template rendering."""

import jinja2
import os
import re

_path = os.path.dirname(os.path.abspath(__file__))


def env():
    """Returns a jinja2 Environment for Fairylab template rendering.

    Returns:
        The jinja2 Environment.
    """
    root = re.sub(r'/common/jinja2_', '', _path)
    ldr = jinja2.FileSystemLoader(root + '/resources/templates')
    ext = ['jinja2.ext.do']

    return jinja2.Environment(
        loader=ldr, extensions=ext, trim_blocks=True, lstrip_blocks=True)
