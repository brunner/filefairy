#!/usr/bin/env python

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/logger', '', _path))
from utils.slack.slack_util import chat_post_message, files_upload, testing_name  # noqa


def log(name, **kwargs):
    s, r, v = [kwargs.get(key, '') for key in ('s', 'r', 'v')]

    if v:
        chat_post_message(testing_name, '(' + name + ') ' + s)
        files_upload(r, name + '.log.txt', testing_name)

    return r
