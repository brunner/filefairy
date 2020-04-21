#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sandbox demo. Non-runnable.

The sandbox is used to do demo rendering.
"""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/impl/dashboard', '', _path))

from api.renderable.renderable import Renderable  # noqa


class Sandbox(Renderable):
    """Sandbox demo."""
    def __init__(self, **kwargs):
        super(Sandbox, self).__init__(**kwargs)

    @staticmethod
    def _href():
        return '/fairylab/sandbox/'

    @staticmethod
    def _title():
        return 'Sandbox'

    def _render_data(self, **kwargs):
        pass
