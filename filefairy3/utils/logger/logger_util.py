#!/usr/bin/env python

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/logger', '', _path))
from utils.slack.slack_util import chat_post_message, files_upload  # noqa


def log(name, **kwargs):
    c, s, v = [kwargs.get(key, '') for key in ('c', 's', 'v')]

    if v:
        chat_post_message('testing', '(' + name + ') ' + s)
        files_upload(c, name + '.log.txt', 'testing')
