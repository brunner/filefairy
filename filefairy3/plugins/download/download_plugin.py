#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import copy
import os
import re
import sys
import threading

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/download', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.serializable.serializable_api import SerializableApi  # noqa
from enums.activity.activity_enum import ActivityEnum  # noqa
from utils.file.file_util import wget_file  # noqa
from utils.unicode.unicode_util import deunicode  # noqa


class DownloadPlugin(PluginApi, SerializableApi):
    def __init__(self, **kwargs):
        super(DownloadPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _info():
        return 'Manages file download and data extraction.'

    def _notify_internal(self, **kwargs):
        activity = kwargs['activity']
        if activity == ActivityEnum.FILE:
            t = threading.Thread(target=self._download)
            t.daemon = True
            t.start()
            return True
        return False

    def _on_message_internal(self, **kwargs):
        return ActivityEnum.NONE

    def _run_internal(self, **kwargs):
        if self.data['downloaded']:
            self.data['downloaded'] = False
            self.write()
            return ActivityEnum.DOWNLOAD

        return ActivityEnum.NONE

    def _setup_internal(self, **kwargs):
        pass

    def _download(self):
        wget_file()
        self._leagues()

        self.data['downloaded'] = True
        self.write()

    def _leagues(self):
        data = self.data
        original = copy.deepcopy(data)

        dpath = os.path.join(_root, 'download/leagues/{}.txt')
        fpath = os.path.join(_root, 'file/news/txt/leagues/league_100_{}.txt')
        for key in sorted(['injuries', 'news', 'transactions']):
            dname = dpath.format(key)
            fname = fpath.format(key)
            if not os.path.isfile(dname) or not os.path.isfile(fname):
                continue
            self._leagues_internal(key, dname, fname)

        if data != original:
            self.write()

    def _leagues_internal(self, key, dname, fname):
        with open(dname, 'r') as df:
            split = df.read()
        with codecs.open(
                fname, 'r', encoding='utf-8', errors='replace') as ff:
            content = deunicode(ff.read())
        if split:
            parts = content.rsplit(split, 1)
            if len(parts) == 2 and parts[1]:
                content = parts[1].strip()
        with open(dname, 'w') as df:
            df.write(content)
