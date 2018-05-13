#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/logger', '', _path))
from util.slack.slack import chat_post_message  # noqa
from util.slack.slack import files_upload  # noqa


def log(name, **kwargs):
    c, s, v = [kwargs.get(key, '') for key in ('c', 's', 'v')]

    if v:
        chat_post_message('testing', '(' + name + ') ' + s)
        if c:
            files_upload(c, name + '.log.txt', 'testing')
