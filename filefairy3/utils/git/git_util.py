#!/usr/bin/env python

import os
import re
import subprocess
import sys

sys.path.append(re.sub(r'/utils/git', '', os.path.dirname(__file__)))
from utils.slack.slack_util import chat_post_message, get_testing_name
from utils.subprocess.subprocess_util import check_output


def pull():
  deb = check_output(['git', 'pull'])
  chat_post_message(get_testing_name(), deb.strip('\n'))


def reset():
  deb = check_output(['git', 'reset', '--hard'])
  chat_post_message(get_testing_name(), deb.strip('\n'))
