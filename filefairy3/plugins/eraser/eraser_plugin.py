#!/usr/bin/env python

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/eraser', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from utils.logger.logger_util import log  # noqa
from utils.slack.slack_util import files_delete, files_list, testing_id  # noqa


class EraserPlugin(PluginApi):
    def __init__(self):
        super(EraserPlugin, self).__init__()

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        pass

    def testing(self, **kwargs):
        obj = files_list(100, testing_id)
        if 'files' in obj:
            for f in obj['files']:
                files_delete(f['id'])
        return log(self._name(), **dict(kwargs, s='Erased testing.'))
