#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess


def check_output(cmd):
    try:
        with open(os.devnull, 'w') as devnull:
            return subprocess.check_output(cmd, stderr=devnull)
    except:
        return ''
