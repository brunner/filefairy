#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from slack_api import call_
import tokens

fs = call_('files.list', {
    'token': tokens.brunnerj,
    'count': 500,
    'channel': 'G3SUFLMK4',
    'user': 'U3ULC7DBP'})

for f in fs['files']:
  call_('files.delete', {'token': tokens.brunnerj, 'file': f['id']})
